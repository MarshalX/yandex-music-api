import SwiftUI

struct LibraryView: View {
    @EnvironmentObject private var catalog: CatalogStore
    @EnvironmentObject private var downloads: DownloadsStore
    @State private var showsAccount = false
    @State private var showsNewPlaylist = false
    @State private var playlistName = ""

    var body: some View {
        NavigationStack {
            Group {
                if let library = catalog.library ?? offlineLibrary {
                    List {
                        Section {
                            NavigationLink {
                                TrackListView(title: "Recently Added", tracks: library.recentlyAdded)
                            } label: {
                                Label("Recently Added", systemImage: "clock")
                            }
                            NavigationLink {
                                TrackListView(title: "Favorites", tracks: library.liked)
                            } label: {
                                Label("Favorites", systemImage: "heart.fill")
                            }
                            NavigationLink {
                                DownloadsView(allTracks: allTracks(in: library))
                            } label: {
                                Label("Downloaded", systemImage: "arrow.down.circle.fill")
                            }
                        }
                        Section("Playlists") {
                            ForEach(library.playlists) { playlist in
                                NavigationLink {
                                    PlaylistView(playlist: playlist)
                                } label: {
                                    HStack(spacing: 12) {
                                        ArtworkView(artwork: playlist.artwork, cornerRadius: 7)
                                            .frame(width: 50, height: 50)
                                        VStack(alignment: .leading, spacing: 3) {
                                            Text(playlist.name)
                                            Text("\(playlist.totalTrackCount ?? playlist.tracks.count) songs")
                                                .font(.caption)
                                                .foregroundStyle(.secondary)
                                        }
                                    }
                                }
                            }
                        }
                    }
                    .listStyle(.insetGrouped)
                } else if catalog.isLoading {
                    ProgressView("Loading library…")
                } else {
                    ContentUnavailableView("Library Is Unavailable", systemImage: "square.stack")
                }
            }
            .navigationTitle("Library")
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button { showsNewPlaylist = true } label: { Image(systemName: "plus") }
                        .accessibilityLabel("New playlist")
                }
                ToolbarItem(placement: .topBarTrailing) {
                    AccountToolbarButton(isPresented: $showsAccount)
                }
            }
            .refreshable { await catalog.refreshLibrary() }
            .sheet(isPresented: $showsAccount) { AccountView() }
            .alert("New Playlist", isPresented: $showsNewPlaylist) {
                TextField("Playlist name", text: $playlistName)
                Button("Cancel", role: .cancel) { playlistName = "" }
                Button("Create") {
                    let name = playlistName.trimmingCharacters(in: .whitespacesAndNewlines)
                    playlistName = ""
                    guard !name.isEmpty else { return }
                    Task { await catalog.createPlaylist(named: name) }
                }
            }
        }
    }

    private var offlineLibrary: MusicLibrary? {
        let tracks = downloads.entries.compactMap(\.track)
        guard !tracks.isEmpty else { return nil }
        return MusicLibrary(recentlyAdded: tracks, liked: [], playlists: [])
    }

    private func allTracks(in library: MusicLibrary) -> [Track] {
        var seen = Set<String>()
        return (library.recentlyAdded + library.liked + library.playlists.flatMap(\.tracks)).filter {
            seen.insert($0.id).inserted
        }
    }
}

struct TrackListView: View {
    @EnvironmentObject private var player: PlayerStore
    @EnvironmentObject private var downloads: DownloadsStore
    let title: String
    let tracks: [Track]

    var body: some View {
        List {
            if !tracks.isEmpty {
                Button { Task { await player.play(tracks[0], queue: tracks) } } label: {
                    Label("Play", systemImage: "play.fill")
                        .frame(maxWidth: .infinity)
                        .font(.headline)
                }
            }
            ForEach(tracks) { track in
                TrackRow(
                    track: track,
                    isDownloaded: downloads.isDownloaded(track),
                    isDownloading: downloads.activeTrackIDs.contains(track.id),
                    play: { Task { await player.play(track, queue: tracks) } },
                    toggleDownload: {
                        Task {
                            if downloads.isDownloaded(track) {
                                await downloads.remove(track)
                            } else {
                                await downloads.download(track, quality: player.preferredQuality)
                            }
                        }
                    }
                )
            }
        }
        .listStyle(.plain)
        .navigationTitle(title)
        .navigationBarTitleDisplayMode(.large)
        .overlay {
            if tracks.isEmpty {
                ContentUnavailableView("No Songs", systemImage: "music.note")
            }
        }
    }
}

struct PlaylistView: View {
    @EnvironmentObject private var catalog: CatalogStore
    @EnvironmentObject private var player: PlayerStore
    @EnvironmentObject private var downloads: DownloadsStore
    private let initialPlaylist: Playlist
    @State private var loaded: Playlist?
    private var playlist: Playlist { loaded ?? initialPlaylist }
    init(playlist: Playlist) { initialPlaylist = playlist }

    var body: some View {
        List {
            Section {
                VStack(spacing: 16) {
                    ArtworkView(artwork: playlist.artwork, cornerRadius: 18)
                        .frame(maxWidth: 280)
                        .aspectRatio(1, contentMode: .fit)
                        .shadow(color: .black.opacity(0.2), radius: 15, y: 8)
                    VStack(spacing: 4) {
                        Text(playlist.name).font(.title2.bold())
                        if let description = playlist.description {
                            Text(description).font(.subheadline).foregroundStyle(.secondary).multilineTextAlignment(.center)
                        }
                    }
                    HStack(spacing: 12) {
                        Button { if let first = playlist.tracks.first { Task { await player.play(first, queue: playlist.tracks) } } } label: {
                            Label("Play", systemImage: "play.fill")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.borderedProminent)
                        Button {
                            if let random = playlist.tracks.randomElement() {
                                player.isShuffling = true
                                Task { await player.play(random, queue: playlist.tracks) }
                            }
                        } label: {
                            Label("Shuffle", systemImage: "shuffle")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                    }
                }
                .listRowBackground(Color.clear)
                .padding(.vertical)
            }

            ForEach(playlist.tracks) { track in
                TrackRow(
                    track: track,
                    isDownloaded: downloads.isDownloaded(track),
                    isDownloading: downloads.activeTrackIDs.contains(track.id),
                    play: { Task { await player.play(track, queue: playlist.tracks) } },
                    toggleDownload: {
                        Task {
                            if downloads.isDownloaded(track) { await downloads.remove(track) }
                            else { await downloads.download(track, quality: player.preferredQuality) }
                        }
                    }
                )
                .swipeActions {
                    if playlist.isEditable {
                        Button("Remove", role: .destructive) {
                            Task {
                                await catalog.remove(track, from: playlist)
                                loaded = await catalog.loadPlaylist(playlist.id)
                            }
                        }
                    }
                }
            }
        }
        .listStyle(.plain)
        .navigationTitle(playlist.name)
        .navigationBarTitleDisplayMode(.inline)
        .task { loaded = await catalog.loadPlaylist(initialPlaylist.id) }
        .refreshable { loaded = await catalog.loadPlaylist(initialPlaylist.id) }
    }
}

struct DownloadsView: View {
    @EnvironmentObject private var downloads: DownloadsStore
    let allTracks: [Track]

    private var downloadedTracks: [Track] {
        downloads.entries.compactMap(\.track)
    }

    var body: some View {
        TrackListView(title: "Downloaded", tracks: downloadedTracks)
            .task { await downloads.refresh() }
    }
}
