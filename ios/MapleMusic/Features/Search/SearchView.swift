import SwiftUI

struct SearchView: View {
    @EnvironmentObject private var catalog: CatalogStore
    @EnvironmentObject private var player: PlayerStore
    @EnvironmentObject private var downloads: DownloadsStore
    @State private var query = ""
    @State private var showsAccount = false

    var body: some View {
        NavigationStack {
            List(catalog.searchResults) { track in
                TrackRow(
                    track: track,
                    isDownloaded: downloads.isDownloaded(track),
                    isDownloading: downloads.activeTrackIDs.contains(track.id),
                    play: { Task { await player.play(track, queue: catalog.searchResults) } },
                    toggleDownload: {
                        Task {
                            if downloads.isDownloaded(track) { await downloads.remove(track) }
                            else { await downloads.download(track, quality: player.preferredQuality) }
                        }
                    }
                )
            }
            .listStyle(.plain)
            .navigationTitle("Search")
            .searchable(text: $query, placement: .navigationBarDrawer(displayMode: .always), prompt: "Artists, songs, albums")
            .onChange(of: query) { _, newValue in catalog.scheduleSearch(newValue) }
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    AccountToolbarButton(isPresented: $showsAccount)
                }
            }
            .sheet(isPresented: $showsAccount) { AccountView() }
            .overlay {
                if catalog.isSearching {
                    ProgressView()
                } else if query.isEmpty {
                    ContentUnavailableView("Find Your Music", systemImage: "magnifyingglass", description: Text("Search by song, artist, or album."))
                } else if catalog.searchResults.isEmpty {
                    ContentUnavailableView.search(text: query)
                }
            }
        }
    }
}
