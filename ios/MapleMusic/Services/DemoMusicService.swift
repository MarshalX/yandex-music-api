import Foundation

actor DemoMusicService: MusicService {
    static let artist = Artist(id: "maple-sessions", name: "Maple Sessions")

    private let tracks: [Track]
    private var playlists: [Playlist]
    private var favoriteTrackIDs: Set<String>

    init() {
        let artist = Self.artist
        let demoTracks = [
            Track(
                id: "northern-lights",
                title: "Northern Lights",
                artist: artist,
                albumTitle: "Afterglow",
                duration: 18,
                artwork: Artwork(colors: ["FF2D55", "7928CA"]),
                availableQualities: [.automatic, .high, .lossless]
            ),
            Track(
                id: "glass-river",
                title: "Glass River",
                artist: artist,
                albumTitle: "Afterglow",
                duration: 18,
                artwork: Artwork(colors: ["0A84FF", "64D2FF"]),
                availableQualities: [.automatic, .high, .lossless]
            ),
            Track(
                id: "midnight-maple",
                title: "Midnight Maple",
                artist: artist,
                albumTitle: "City Rooms",
                duration: 18,
                artwork: Artwork(colors: ["BF5AF2", "FF9F0A"]),
                availableQualities: [.automatic, .high, .lossless]
            ),
            Track(
                id: "soft-static",
                title: "Soft Static",
                artist: artist,
                albumTitle: "City Rooms",
                duration: 18,
                artwork: Artwork(colors: ["30D158", "004E64"]),
                availableQualities: [.automatic, .high, .lossless]
            ),
        ]
        tracks = demoTracks
        favoriteTrackIDs = Set(demoTracks.prefix(2).map(\.id))
        playlists = [
            Playlist(
                id: "demo-favorites",
                name: "Maple Essentials",
                description: "A small offline-ready demo playlist.",
                artwork: Artwork(colors: ["FF375F", "5E5CE6"]),
                tracks: demoTracks,
                isEditable: true
            )
        ]
    }

    func home() async throws -> HomeFeed {
        HomeFeed(
            greeting: Self.greeting,
            featured: Array(tracks.prefix(3)),
            shelves: [
                MusicShelf(
                    id: "made-for-you",
                    title: "Made for You",
                    subtitle: "A telemetry-free local demo",
                    layout: .cards,
                    tracks: tracks
                ),
                MusicShelf(
                    id: "recently-played",
                    title: "Recently Played",
                    subtitle: nil,
                    layout: .list,
                    tracks: Array(tracks.reversed())
                ),
            ]
        )
    }

    func search(query: String) async throws -> [Track] {
        let normalized = query.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        guard !normalized.isEmpty else { return [] }
        return tracks.filter {
            $0.title.lowercased().contains(normalized)
                || $0.artist.name.lowercased().contains(normalized)
                || $0.albumTitle.lowercased().contains(normalized)
        }
    }

    func library() async throws -> MusicLibrary {
        MusicLibrary(
            recentlyAdded: tracks,
            liked: tracks.filter { favoriteTrackIDs.contains($0.id) },
            playlists: playlists
        )
    }

    func playlist(id: String) async throws -> Playlist {
        guard let playlist = playlists.first(where: { $0.id == id }) else {
            throw MusicServiceError.http(404)
        }
        return playlist
    }

    func createPlaylist(name: String) async throws -> Playlist {
        let playlist = Playlist(
            id: UUID().uuidString,
            name: name,
            description: nil,
            artwork: Artwork(colors: ["FF375F", "FF9F0A"]),
            tracks: [],
            isEditable: true
        )
        playlists.append(playlist)
        return playlist
    }

    func add(trackID: String, toPlaylistID playlistID: String) async throws {
        guard let track = tracks.first(where: { $0.id == trackID }),
              let index = playlists.firstIndex(where: { $0.id == playlistID })
        else { throw MusicServiceError.http(404) }
        if !playlists[index].tracks.contains(where: { $0.id == trackID }) {
            playlists[index].tracks.append(track)
        }
    }

    func remove(trackID: String, fromPlaylistID playlistID: String) async throws {
        guard let index = playlists.firstIndex(where: { $0.id == playlistID }) else {
            throw MusicServiceError.http(404)
        }
        playlists[index].tracks.removeAll { $0.id == trackID }
    }

    func setFavorite(trackID: String, isFavorite: Bool) async throws {
        guard tracks.contains(where: { $0.id == trackID }) else {
            throw MusicServiceError.http(404)
        }
        if isFavorite {
            favoriteTrackIDs.insert(trackID)
        } else {
            favoriteTrackIDs.remove(trackID)
        }
    }

    func playbackAsset(for track: Track, quality: AudioQuality) async throws -> PlaybackAsset {
        let bundle: Bundle
#if SWIFT_PACKAGE
        bundle = .module
#else
        bundle = .main
#endif
        guard let url = bundle.url(forResource: track.id, withExtension: "wav", subdirectory: "DemoAudio")
            ?? bundle.url(forResource: track.id, withExtension: "wav")
        else {
            throw MusicServiceError.offlineUnavailable
        }
        let resolvedQuality: AudioQuality = quality == .automatic ? .high : quality
        return PlaybackAsset(
            url: url,
            quality: resolvedQuality,
            codec: "Linear PCM",
            bitDepth: 16,
            sampleRate: 44_100,
            expiresAt: nil,
            allowsOfflineDownload: true
        )
    }

    func lyrics(for track: Track) async throws -> Lyrics? {
        let words: [String]
        switch track.id {
        case "northern-lights":
            words = ["City asleep under silver skies", "A quiet pulse and the streetlight sighs", "Hold the moment, let it arrive", "Northern lights in the back of our minds"]
        case "glass-river":
            words = ["Every reflection starts to move", "Glass river carrying the blue", "Nothing to chase and nothing to prove", "Just let the current carry you"]
        case "midnight-maple":
            words = ["Late train humming below the room", "Maple shadows and violet bloom", "Turn down the noise, turn up the tune", "We have a little more night to use"]
        default:
            words = ["Soft static filling the air", "A tiny signal says you are there", "No grand ending, no perfect line", "Only the rhythm keeping the time"]
        }
        return Lyrics(
            trackID: track.id,
            writers: "Maple Sessions",
            lines: words.enumerated().map { index, text in
                LyricsLine(time: Double(index) * 4.0, text: text)
            }
        )
    }

    private static var greeting: String {
        switch Calendar.current.component(.hour, from: Date()) {
        case 5 ..< 12: "Good Morning"
        case 12 ..< 18: "Good Afternoon"
        default: "Good Evening"
        }
    }
}
