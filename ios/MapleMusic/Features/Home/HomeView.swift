import SwiftUI

struct HomeView: View {
    @EnvironmentObject private var catalog: CatalogStore
    @EnvironmentObject private var player: PlayerStore
    @EnvironmentObject private var auth: AuthStore
    @State private var showsAccount = false

    var body: some View {
        NavigationStack {
            Group {
                if let home = catalog.home {
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 28) {
                            featured(home.featured)
                            ForEach(home.shelves) { shelf in
                                shelfView(shelf)
                            }
                        }
                        .padding(.bottom, 20)
                    }
                } else if catalog.isLoading {
                    ProgressView("Loading your music…")
                } else if auth.state == .signedOut {
                    ContentUnavailableView {
                        Label("Your Music Starts Here", systemImage: "music.note.house")
                    } description: {
                        Text("Connect your account or choose Local Demo in Settings.")
                    } actions: {
                        Button("Open Settings") { showsAccount = true }
                            .buttonStyle(.borderedProminent)
                    }
                } else {
                    ContentUnavailableView(
                        "Home Is Unavailable",
                        systemImage: "music.note.house",
                        description: Text(catalog.errorMessage ?? "Try again in a moment.")
                    )
                }
            }
            .navigationTitle(catalog.home?.greeting ?? "Home")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    AccountToolbarButton(isPresented: $showsAccount)
                }
            }
            .refreshable { await catalog.bootstrap() }
            .sheet(isPresented: $showsAccount) { AccountView() }
        }
    }

    private func featured(_ tracks: [Track]) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Listen Now")
                .font(.title2.bold())
                .padding(.horizontal)
            ScrollView(.horizontal, showsIndicators: false) {
                LazyHStack(spacing: 16) {
                    ForEach(tracks) { track in
                        Button { Task { await player.play(track, queue: tracks) } } label: {
                            VStack(alignment: .leading, spacing: 8) {
                                ArtworkView(artwork: track.artwork, cornerRadius: 14)
                                    .frame(width: 260, height: 260)
                                    .shadow(color: .black.opacity(0.18), radius: 12, y: 7)
                                Text(track.title).font(.headline).foregroundStyle(.primary).lineLimit(1)
                                Text(track.artist.name).font(.subheadline).foregroundStyle(.secondary).lineLimit(1)
                            }
                            .frame(width: 260, alignment: .leading)
                        }
                        .buttonStyle(.plain)
                        .contextMenu { TrackActions(track: track) }
                    }
                }
                .padding(.horizontal)
            }
        }
    }

    @ViewBuilder
    private func shelfView(_ shelf: MusicShelf) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            VStack(alignment: .leading, spacing: 2) {
                Text(shelf.title).font(.title2.bold())
                if let subtitle = shelf.subtitle {
                    Text(subtitle).font(.subheadline).foregroundStyle(.secondary)
                }
            }
            .padding(.horizontal)

            if shelf.layout == .cards {
                ScrollView(.horizontal, showsIndicators: false) {
                    LazyHStack(spacing: 14) {
                        ForEach(shelf.tracks) { track in
                            Button { Task { await player.play(track, queue: shelf.tracks) } } label: {
                                VStack(alignment: .leading, spacing: 7) {
                                    ArtworkView(artwork: track.artwork)
                                        .frame(width: 156, height: 156)
                                    Text(track.title).font(.subheadline.weight(.medium)).foregroundStyle(.primary).lineLimit(1)
                                    Text(track.artist.name).font(.caption).foregroundStyle(.secondary).lineLimit(1)
                                }
                                .frame(width: 156, alignment: .leading)
                            }
                            .buttonStyle(.plain)
                            .contextMenu { TrackActions(track: track) }
                        }
                    }
                    .padding(.horizontal)
                }
            } else {
                VStack(spacing: 0) {
                    ForEach(shelf.tracks) { track in
                        CompactTrackRow(track: track, queue: shelf.tracks)
                        if track.id != shelf.tracks.last?.id { Divider().padding(.leading, 76) }
                    }
                }
                .padding(.horizontal)
            }
        }
    }
}

private struct CompactTrackRow: View {
    @EnvironmentObject private var player: PlayerStore
    let track: Track
    let queue: [Track]

    var body: some View {
        Button { Task { await player.play(track, queue: queue) } } label: {
            HStack(spacing: 12) {
                ArtworkView(artwork: track.artwork, cornerRadius: 7).frame(width: 52, height: 52)
                VStack(alignment: .leading, spacing: 3) {
                    Text(track.title).foregroundStyle(.primary).lineLimit(1)
                    Text(track.artist.name).font(.subheadline).foregroundStyle(.secondary).lineLimit(1)
                }
                Spacer()
                Image(systemName: "ellipsis").foregroundStyle(.secondary).padding(.horizontal, 8)
            }
            .padding(.vertical, 6)
        }
        .buttonStyle(.plain)
        .contextMenu { TrackActions(track: track) }
    }
}
