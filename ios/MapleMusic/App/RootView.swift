import SwiftUI

struct RootView: View {
    private enum Tab: Hashable {
        case home
        case library
        case search
    }

    @EnvironmentObject private var player: PlayerStore
    @EnvironmentObject private var catalog: CatalogStore
    @EnvironmentObject private var downloads: DownloadsStore
    @State private var selection: Tab = .home

    var body: some View {
        TabView(selection: $selection) {
            HomeView()
                .tabItem { Label("Home", systemImage: "house.fill") }
                .tag(Tab.home)

            LibraryView()
                .tabItem { Label("Library", systemImage: "square.stack.fill") }
                .tag(Tab.library)

            SearchView()
                .tabItem { Label("Search", systemImage: "magnifyingglass") }
                .tag(Tab.search)
        }
        .safeAreaInset(edge: .bottom, spacing: 0) {
            if let track = player.currentTrack {
                MiniPlayerView(track: track)
                    .padding(.horizontal, 8)
                    .padding(.bottom, 2)
            }
        }
        .sheet(isPresented: $player.isShowingNowPlaying) {
            NowPlayingView()
        }
        .alert("Music Service", isPresented: Binding(
            get: { catalog.errorMessage != nil || downloads.errorMessage != nil },
            set: { if !$0 { catalog.errorMessage = nil; downloads.errorMessage = nil } }
        )) { Button("OK", role: .cancel) { catalog.errorMessage = nil; downloads.errorMessage = nil } } message: {
            Text(downloads.errorMessage ?? catalog.errorMessage ?? "")
        }
        .alert("Playback Error", isPresented: Binding(
            get: { player.errorMessage != nil },
            set: { if !$0 { player.errorMessage = nil } }
        )) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(player.errorMessage ?? "Unknown error")
        }
    }
}

struct MiniPlayerView: View {
    @EnvironmentObject private var player: PlayerStore
    let track: Track

    var body: some View {
        HStack(spacing: 11) {
            ArtworkView(artwork: track.artwork, cornerRadius: 7)
                .frame(width: 44, height: 44)
            VStack(alignment: .leading, spacing: 2) {
                Text(track.title).font(.subheadline.weight(.semibold)).lineLimit(1)
                Text(track.artist.name).font(.caption).foregroundStyle(.secondary).lineLimit(1)
            }
            Spacer()
            if player.isBuffering { ProgressView().controlSize(.small) }
            Button { player.togglePlayback() } label: {
                Image(systemName: player.isPlaying ? "pause.fill" : "play.fill")
                    .font(.title3)
                    .frame(width: 36, height: 36)
            }
            Button { player.next() } label: {
                Image(systemName: "forward.fill")
                    .font(.body)
                    .frame(width: 34, height: 36)
            }
        }
        .padding(6)
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 13, style: .continuous))
        .overlay(alignment: .bottom) {
            GeometryReader { proxy in
                Capsule()
                    .fill(Color.mapleAccent)
                    .frame(width: proxy.size.width * player.progress, height: 2)
            }
            .frame(height: 2)
            .padding(.horizontal, 10)
        }
        .contentShape(RoundedRectangle(cornerRadius: 13, style: .continuous))
        .onTapGesture { player.isShowingNowPlaying = true }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("Now playing \(track.title) by \(track.artist.name)")
        .accessibilityAction { player.isShowingNowPlaying = true }
    }
}
