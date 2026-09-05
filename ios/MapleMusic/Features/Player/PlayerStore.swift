import AVFoundation
import Foundation
import MediaPlayer
import Combine

@MainActor
final class PlayerStore: ObservableObject {
    @Published private(set) var currentTrack: Track?
    @Published private(set) var queue: [Track] = []
    @Published private(set) var isPlaying = false
    @Published private(set) var currentTime: TimeInterval = 0
    @Published private(set) var duration: TimeInterval = 0
    @Published private(set) var resolvedAsset: PlaybackAsset?
    @Published private(set) var lyrics: Lyrics?
    @Published var preferredQuality: AudioQuality {
        didSet { UserDefaults.standard.set(preferredQuality.rawValue, forKey: "preferred-quality") }
    }
    @Published var repeatMode: RepeatMode = .off
    @Published var isShuffling = false
    @Published var isShowingNowPlaying = false
    @Published var errorMessage: String?
    @Published private(set) var isBuffering = false

    private let service: AnyMusicService
    private let offlineStore: OfflineStore
    private let player = AVPlayer()
    private var timeObserver: Any?
    private var endObserver: NSObjectProtocol?
    private var itemStatus: NSKeyValueObservation?
    private var requestID = UUID()
    private var playbackFile: URL?
    private var remoteTargets: [(MPRemoteCommand, Any)] = []

    init(service: AnyMusicService, offlineStore: OfflineStore) {
        self.service = service
        self.offlineStore = offlineStore
        preferredQuality = AudioQuality(rawValue: UserDefaults.standard.string(forKey: "preferred-quality") ?? "") ?? .automatic
        configureAudioSession()
        configureObservers()
        configureRemoteCommands()
    }

    deinit {
        if let timeObserver {
            player.removeTimeObserver(timeObserver)
        }
        if let endObserver {
            NotificationCenter.default.removeObserver(endObserver)
        }
    }

    var progress: Double {
        guard duration > 0 else { return 0 }
        return min(max(currentTime / duration, 0), 1)
    }

    var activeLyricsLineIndex: Int? {
        guard let lines = lyrics?.lines, !lines.isEmpty else { return nil }
        return LyricsSynchronizer.activeLineIndex(at: currentTime, lines: lines)
    }

    func play(_ track: Track, queue proposedQueue: [Track]? = nil) async {
        let identifier = UUID()
        requestID = identifier
        player.pause()
        player.replaceCurrentItem(with: nil)
        if let playbackFile { try? FileManager.default.removeItem(at: playbackFile) }
        playbackFile = nil
        resolvedAsset = nil
        isPlaying = false
        isBuffering = true
        errorMessage = nil
        if let proposedQueue, !proposedQueue.isEmpty {
            queue = proposedQueue
        } else if !queue.contains(where: { $0.id == track.id }) {
            queue = [track]
        }
        currentTrack = track
        duration = track.duration
        currentTime = 0
        lyrics = nil
        updateNowPlayingInfo()
        do {
            let asset: PlaybackAsset
            if let offline = await offlineStore.localAsset(for: track) {
                asset = offline
            } else {
                asset = try await service.playbackAsset(for: track, quality: resolvedPreferredQuality(for: track))
            }
            guard requestID == identifier else { return }
            var playbackURL = asset.url
            if asset.decryptionKey != nil {
                let file = FileManager.default.temporaryDirectory.appendingPathComponent("maple-\(identifier).\(MediaFileLoader.fileExtension(for: asset))")
                try await MediaFileLoader.download(asset, to: file)
                guard requestID == identifier else { try? FileManager.default.removeItem(at: file); return }
                playbackFile = file
                playbackURL = file
            }
            resolvedAsset = asset
            let item = AVPlayerItem(url: playbackURL)
            itemStatus = item.observe(\.status, options: [.new]) { [weak self] observed, _ in
                let status = observed.status
                let message = observed.error?.localizedDescription
                Task { @MainActor in
                    guard let self, self.requestID == identifier else { return }
                    self.isBuffering = status == .unknown
                    if status == .failed { self.pause(); self.errorMessage = message ?? "Playback failed." }
                }
            }
            player.replaceCurrentItem(with: item)
            player.play()
            isPlaying = true
            updateNowPlayingInfo()
            Task {
                let cached = await offlineStore.localLyrics(for: track.id)
                let fetched: Lyrics?
                if let cached { fetched = cached } else { fetched = try? await service.lyrics(for: track) }
                guard requestID == identifier else { return }
                lyrics = fetched
            }
        } catch {
            guard requestID == identifier else { return }
            isPlaying = false
            isBuffering = false
            resolvedAsset = nil
            errorMessage = error.localizedDescription
            updateNowPlayingInfo()
        }
    }

    func stop() {
        requestID = UUID()
        player.pause()
        player.replaceCurrentItem(with: nil)
        itemStatus = nil
        isPlaying = false
        isBuffering = false
        currentTrack = nil
        queue = []
        lyrics = nil
        resolvedAsset = nil
        if let playbackFile { try? FileManager.default.removeItem(at: playbackFile) }
        playbackFile = nil
        for (command, target) in remoteTargets { command.removeTarget(target) }
        remoteTargets = []
        updateNowPlayingInfo()
    }

    func togglePlayback() {
        isPlaying ? pause() : resume()
    }

    func resume() {
        guard player.currentItem != nil else {
            if let currentTrack { Task { await play(currentTrack) } }
            return
        }
        player.play()
        isPlaying = true
        updateNowPlayingInfo()
    }

    func pause() {
        player.pause()
        isPlaying = false
        updateNowPlayingInfo()
    }

    func seek(to time: TimeInterval) {
        let target = min(max(time, 0), duration)
        player.seek(to: CMTime(seconds: target, preferredTimescale: 600), toleranceBefore: .zero, toleranceAfter: .zero)
        currentTime = target
        updateNowPlayingInfo()
    }

    func next() {
        guard let currentTrack, !queue.isEmpty else { return }
        let nextTrack: Track?
        if isShuffling {
            nextTrack = queue.filter { $0.id != currentTrack.id }.randomElement() ?? currentTrack
        } else if let index = queue.firstIndex(where: { $0.id == currentTrack.id }), index + 1 < queue.count {
            nextTrack = queue[index + 1]
        } else if repeatMode == .all {
            nextTrack = queue.first
        } else {
            nextTrack = nil
        }
        if let nextTrack { Task { await play(nextTrack) } } else { pause() }
    }

    func previous() {
        if currentTime > 3 {
            seek(to: 0)
            return
        }
        guard let currentTrack,
              let index = queue.firstIndex(where: { $0.id == currentTrack.id }),
              index > 0
        else {
            seek(to: 0)
            return
        }
        Task { await play(queue[index - 1]) }
    }

    func cycleRepeatMode() {
        switch repeatMode {
        case .off: repeatMode = .all
        case .all: repeatMode = .one
        case .one: repeatMode = .off
        }
    }

    private func resolvedPreferredQuality(for track: Track) -> AudioQuality {
        if preferredQuality == .automatic { return .automatic }
        if track.availableQualities.contains(preferredQuality) { return preferredQuality }
        return track.availableQualities.contains(.high) ? .high : .automatic
    }

    private func handleEnd() {
        if repeatMode == .one {
            seek(to: 0)
            resume()
        } else {
            next()
        }
    }

    private func configureAudioSession() {
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .default, options: [.allowAirPlay, .allowBluetoothA2DP])
            try session.setActive(true)
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    private func configureObservers() {
        timeObserver = player.addPeriodicTimeObserver(
            forInterval: CMTime(seconds: 0.25, preferredTimescale: 600),
            queue: .main
        ) { [weak self] time in
            Task { @MainActor in
                guard let self else { return }
                self.currentTime = time.seconds.isFinite ? max(time.seconds, 0) : 0
                if let seconds = self.player.currentItem?.duration.seconds, seconds.isFinite, seconds > 0 {
                    self.duration = seconds
                }
                self.updateNowPlayingInfo()
            }
        }
        endObserver = NotificationCenter.default.addObserver(
            forName: .AVPlayerItemDidPlayToEndTime,
            object: nil,
            queue: .main
        ) { [weak self] notification in
            Task { @MainActor in
                guard let self,
                      let endedItem = notification.object as? AVPlayerItem,
                      let currentItem = self.player.currentItem,
                      endedItem === currentItem
                else { return }
                self.handleEnd()
            }
        }
    }

    private func configureRemoteCommands() {
        let center = MPRemoteCommandCenter.shared()
        remoteTargets.append((center.playCommand, center.playCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.resume() }
            return .success
        }))
        remoteTargets.append((center.pauseCommand, center.pauseCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.pause() }
            return .success
        }))
        remoteTargets.append((center.togglePlayPauseCommand, center.togglePlayPauseCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.togglePlayback() }
            return .success
        }))
        remoteTargets.append((center.nextTrackCommand, center.nextTrackCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.next() }
            return .success
        }))
        remoteTargets.append((center.previousTrackCommand, center.previousTrackCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.previous() }
            return .success
        }))
        remoteTargets.append((center.changePlaybackPositionCommand, center.changePlaybackPositionCommand.addTarget { [weak self] event in
            guard let event = event as? MPChangePlaybackPositionCommandEvent else { return .commandFailed }
            Task { @MainActor in self?.seek(to: event.positionTime) }
            return .success
        }))
    }

    private func updateNowPlayingInfo() {
        guard let track = currentTrack else {
            MPNowPlayingInfoCenter.default().nowPlayingInfo = nil
            return
        }
        MPNowPlayingInfoCenter.default().nowPlayingInfo = [
            MPMediaItemPropertyTitle: track.title,
            MPMediaItemPropertyArtist: track.artist.name,
            MPMediaItemPropertyAlbumTitle: track.albumTitle,
            MPMediaItemPropertyPlaybackDuration: duration,
            MPNowPlayingInfoPropertyElapsedPlaybackTime: currentTime,
            MPNowPlayingInfoPropertyPlaybackRate: isPlaying ? 1.0 : 0.0,
        ]
    }
}

enum LyricsSynchronizer {
    static func activeLineIndex(at time: TimeInterval, lines: [LyricsLine]) -> Int? {
        guard !lines.isEmpty, time >= lines[0].time else { return nil }
        var lower = 0
        var upper = lines.count
        while lower < upper {
            let middle = (lower + upper) / 2
            if lines[middle].time <= time {
                lower = middle + 1
            } else {
                upper = middle
            }
        }
        return max(0, lower - 1)
    }
}
