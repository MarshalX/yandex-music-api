import Foundation
import Combine

@MainActor
final class CatalogStore: ObservableObject {
    @Published private(set) var home: HomeFeed?
    @Published private(set) var library: MusicLibrary?
    @Published private(set) var searchResults: [Track] = []
    @Published private(set) var isLoading = false
    @Published private(set) var isSearching = false
    @Published var errorMessage: String?

    private let service: AnyMusicService
    private var searchTask: Task<Void, Never>?

    init(service: AnyMusicService) {
        self.service = service
    }

    func bootstrap() async {
        isLoading = true
        errorMessage = nil
        do { home = try await service.home() } catch { errorMessage = error.localizedDescription }
        await refreshLibrary()
        isLoading = false
    }

    func refreshLibrary() async {
        do {
            library = try await service.library()
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    func scheduleSearch(_ query: String) {
        searchTask?.cancel()
        let trimmed = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else {
            searchResults = []
            isSearching = false
            return
        }
        isSearching = true
        searchTask = Task {
            try? await Task.sleep(for: .milliseconds(300))
            guard !Task.isCancelled else { return }
            do {
                let results = try await service.search(query: trimmed)
                guard !Task.isCancelled else { return }
                searchResults = results
                errorMessage = nil
            } catch is CancellationError {
                return
            } catch {
                guard !Task.isCancelled else { return }
                searchResults = []
                errorMessage = error.localizedDescription
            }
            isSearching = false
        }
    }

    func createPlaylist(named name: String) async {
        do {
            let playlist = try await service.createPlaylist(name: name)
            if var snapshot = library {
                snapshot = MusicLibrary(
                    recentlyAdded: snapshot.recentlyAdded,
                    liked: snapshot.liked,
                    playlists: snapshot.playlists + [playlist]
                )
                library = snapshot
            } else {
                await refreshLibrary()
            }
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    func loadPlaylist(_ id: String) async -> Playlist? {
        do { return try await service.playlist(id: id) }
        catch { errorMessage = error.localizedDescription; return nil }
    }
    func add(_ track: Track, to playlist: Playlist) async {
        do { try await service.add(trackID: track.id, toPlaylistID: playlist.id); await refreshLibrary() }
        catch { errorMessage = error.localizedDescription }
    }
    func remove(_ track: Track, from playlist: Playlist) async {
        do { try await service.remove(trackID: track.id, fromPlaylistID: playlist.id); await refreshLibrary() }
        catch { errorMessage = error.localizedDescription }
    }
    func isFavorite(_ track: Track) -> Bool { library?.liked.contains { $0.id == track.id } ?? false }
    func toggleFavorite(_ track: Track) async {
        do { try await service.setFavorite(trackID: track.id, isFavorite: !isFavorite(track)); await refreshLibrary() }
        catch { errorMessage = error.localizedDescription }
    }
}
