import AVKit
import SwiftUI

struct NowPlayingView: View {
    private enum Page: String, CaseIterable, Identifiable {
        case player = "Playing"
        case lyrics = "Lyrics"
        case queue = "Queue"
        var id: Self { self }
    }

    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject private var player: PlayerStore
    @EnvironmentObject private var downloads: DownloadsStore
    @State private var page: Page = .player

    var body: some View {
        ZStack {
            background
            VStack(spacing: 12) {
                header
                Picker("Now Playing Page", selection: $page) {
                    ForEach(Page.allCases) { page in Text(page.rawValue).tag(page) }
                }
                .pickerStyle(.segmented)
                .padding(.horizontal, 22)

                Group {
                    switch page {
                    case .player: playerPage
                    case .lyrics: LyricsView()
                    case .queue: QueueView()
                    }
                }
                .transition(.opacity)
            }
        }
        .animation(.easeInOut(duration: 0.2), value: page)
        .preferredColorScheme(.dark)
    }

    private var background: some View {
        Group {
            if let artwork = player.currentTrack?.artwork {
                LinearGradient(
                    colors: artwork.colors.map(Color.init(hex:)) + [.black],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            } else {
                LinearGradient(colors: [.mapleSecondary, .black], startPoint: .top, endPoint: .bottom)
            }
        }
        .overlay(.black.opacity(0.25))
        .ignoresSafeArea()
    }

    private var header: some View {
        HStack {
            Button { dismiss() } label: {
                Image(systemName: "chevron.down").font(.headline).frame(width: 40, height: 40)
            }
            Spacer()
            VStack(spacing: 1) {
                Text("NOW PLAYING").font(.caption2.bold()).foregroundStyle(.white.opacity(0.65))
                Text(player.currentTrack?.albumTitle ?? "Maple Music").font(.caption).lineLimit(1)
            }
            Spacer()
            Menu {
                Picker("Quality", selection: $player.preferredQuality) {
                    ForEach(AudioQuality.allCases) { Text($0.title).tag($0) }
                }
                if let track = player.currentTrack {
                    TrackActions(track: track)
                    if downloads.isDownloaded(track) {
                        Button("Remove Download", systemImage: "trash", role: .destructive) {
                            Task { await downloads.remove(track) }
                        }
                    } else if track.downloadAllowed {
                        Button("Download", systemImage: "arrow.down.circle") {
                            Task { await downloads.download(track, quality: player.preferredQuality) }
                        }
                    }
                }
            } label: {
                Image(systemName: "ellipsis.circle").font(.title3).frame(width: 40, height: 40)
            }
        }
        .padding(.horizontal, 10)
        .foregroundStyle(.white)
    }

    private var playerPage: some View {
        GeometryReader { proxy in
            let artworkSide = min(proxy.size.width - 48, proxy.size.height * 0.48)
            VStack(spacing: 0) {
                Spacer(minLength: 12)
                if let track = player.currentTrack {
                    ArtworkView(artwork: track.artwork, cornerRadius: 20)
                        .frame(width: artworkSide, height: artworkSide)
                        .shadow(color: .black.opacity(0.42), radius: 28, y: 18)
                        .scaleEffect(player.isPlaying ? 1 : 0.92)
                        .animation(.spring(response: 0.45, dampingFraction: 0.8), value: player.isPlaying)
                }
                Spacer(minLength: 24)
                metadata
                scrubber
                controls
                footerControls
                Spacer(minLength: 12)
            }
            .frame(maxWidth: .infinity)
            .padding(.horizontal, 26)
        }
    }

    private var metadata: some View {
        HStack {
            if player.isBuffering { ProgressView().tint(.white) }
            VStack(alignment: .leading, spacing: 3) {
                Text(player.currentTrack?.title ?? "Nothing Playing")
                    .font(.title3.bold())
                    .lineLimit(1)
                Text(player.currentTrack?.artist.name ?? "")
                    .font(.title3)
                    .foregroundStyle(.white.opacity(0.68))
                    .lineLimit(1)
            }
            Spacer()
            if let asset = player.resolvedAsset {
                VStack(alignment: .trailing, spacing: 2) {
                    Text(asset.quality == .lossless ? "LOSSLESS" : asset.quality.title.uppercased())
                        .font(.caption2.bold())
                    Text(asset.codec).font(.caption2).foregroundStyle(.white.opacity(0.65))
                }
            }
        }
        .foregroundStyle(.white)
    }

    private var scrubber: some View {
        VStack(spacing: 3) {
            Slider(
                value: Binding(get: { player.currentTime }, set: player.seek),
                in: 0 ... max(player.duration, 1)
            )
            .tint(.white)
            HStack {
                Text(player.currentTime.musicTime)
                Spacer()
                Text("-\(max(player.duration - player.currentTime, 0).musicTime)")
            }
            .font(.caption2.monospacedDigit())
            .foregroundStyle(.white.opacity(0.62))
        }
        .padding(.top, 20)
    }

    private var controls: some View {
        HStack {
            Button { player.previous() } label: {
                Image(systemName: "backward.fill").font(.system(size: 32))
            }
            Spacer()
            Button { player.togglePlayback() } label: {
                Image(systemName: player.isPlaying ? "pause.fill" : "play.fill")
                    .font(.system(size: 46, weight: .medium))
                    .frame(width: 74, height: 74)
            }
            Spacer()
            Button { player.next() } label: {
                Image(systemName: "forward.fill").font(.system(size: 32))
            }
        }
        .foregroundStyle(.white)
        .padding(.horizontal, 22)
        .padding(.top, 10)
    }

    private var footerControls: some View {
        HStack {
            Button { player.isShuffling.toggle() } label: {
                Image(systemName: "shuffle")
                    .foregroundStyle(player.isShuffling ? Color.mapleAccent : .white)
            }
            Spacer()
            Button { page = .lyrics } label: { Image(systemName: "quote.bubble") }
            Spacer()
            AirPlayButton().frame(width: 28, height: 28)
            Spacer()
            Button { player.cycleRepeatMode() } label: {
                Image(systemName: player.repeatMode == .one ? "repeat.1" : "repeat")
                    .foregroundStyle(player.repeatMode == .off ? .white : Color.mapleAccent)
            }
            Spacer()
            Button { page = .queue } label: { Image(systemName: "list.bullet") }
        }
        .font(.title3)
        .foregroundStyle(.white)
        .padding(.horizontal, 6)
        .padding(.top, 18)
    }
}

private struct LyricsView: View {
    @EnvironmentObject private var player: PlayerStore

    var body: some View {
        Group {
            if let lyrics = player.lyrics, !lyrics.lines.isEmpty {
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 20) {
                            ForEach(Array(lyrics.lines.enumerated()), id: \.element.id) { index, line in
                                Button { player.seek(to: line.time) } label: {
                                    Text(line.text)
                                        .font(.title2.bold())
                                        .multilineTextAlignment(.leading)
                                        .foregroundStyle(index == player.activeLyricsLineIndex ? .white : .white.opacity(0.38))
                                        .scaleEffect(index == player.activeLyricsLineIndex ? 1 : 0.98, anchor: .leading)
                                }
                                .buttonStyle(.plain)
                                .id(index)
                            }
                            if let writers = lyrics.writers {
                                Text("Written by \(writers)")
                                    .font(.caption)
                                    .foregroundStyle(.white.opacity(0.45))
                                    .padding(.top, 16)
                            }
                        }
                        .padding(24)
                    }
                    .onChange(of: player.activeLyricsLineIndex) { _, index in
                        guard let index else { return }
                        withAnimation(.easeOut(duration: 0.35)) {
                            proxy.scrollTo(index, anchor: .center)
                        }
                    }
                }
            } else {
                ContentUnavailableView("Lyrics Unavailable", systemImage: "quote.bubble", description: Text("Lyrics will appear when the provider supplies licensed text."))
                    .foregroundStyle(.white)
            }
        }
    }
}

private struct QueueView: View {
    @EnvironmentObject private var player: PlayerStore

    var body: some View {
        List(player.queue) { track in
            Button { Task { await player.play(track) } } label: {
                HStack(spacing: 12) {
                    ArtworkView(artwork: track.artwork, cornerRadius: 7).frame(width: 48, height: 48)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(track.title).foregroundStyle(.white)
                        Text(track.artist.name).font(.caption).foregroundStyle(.white.opacity(0.6))
                    }
                    Spacer()
                    if player.currentTrack?.id == track.id {
                        Image(systemName: "waveform").foregroundStyle(Color.mapleAccent)
                    }
                }
            }
            .listRowBackground(Color.clear)
        }
        .listStyle(.plain)
        .scrollContentBackground(.hidden)
    }
}

private struct AirPlayButton: UIViewRepresentable {
    func makeUIView(context: Context) -> AVRoutePickerView {
        let view = AVRoutePickerView()
        view.tintColor = .white
        view.activeTintColor = UIColor(Color.mapleAccent)
        return view
    }

    func updateUIView(_ uiView: AVRoutePickerView, context: Context) {}
}
