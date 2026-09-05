import Foundation
import Combine

@MainActor
final class DownloadsStore: ObservableObject {
    @Published private(set) var entries: [OfflineEntry] = []
    @Published private(set) var activeTrackIDs: Set<String> = []
    @Published var errorMessage: String?

    private let offlineStore: OfflineStore
    private let service: AnyMusicService

    init(offlineStore: OfflineStore, service: AnyMusicService) {
        self.offlineStore = offlineStore
        self.service = service
    }

    func refresh() async {
        entries = await offlineStore.entries()
    }

    func isDownloaded(_ track: Track) -> Bool {
        entries.contains { $0.trackID == track.id }
    }

    func download(_ track: Track, quality: AudioQuality) async {
        guard !activeTrackIDs.contains(track.id) else { return }
        activeTrackIDs.insert(track.id)
        errorMessage = nil
        defer { activeTrackIDs.remove(track.id) }
        do {
            let asset = try await service.playbackAsset(for: track, quality: quality)
            let lyrics = try? await service.lyrics(for: track)
            try await offlineStore.save(track: track, asset: asset, lyrics: lyrics)
            await refresh()
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    func remove(_ track: Track) async {
        do {
            try await offlineStore.remove(trackID: track.id)
            await refresh()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
