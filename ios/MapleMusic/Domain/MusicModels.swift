import Foundation

enum AudioQuality: String, Codable, CaseIterable, Identifiable, Sendable {
    case automatic
    case high
    case lossless

    var id: Self { self }

    var title: String {
        switch self {
        case .automatic: "Automatic"
        case .high: "High Quality"
        case .lossless: "Lossless"
        }
    }

    var subtitle: String {
        switch self {
        case .automatic: "Adapts to your connection"
        case .high: "Up to 320 kbps"
        case .lossless: "ALAC or FLAC when available"
        }
    }
}

enum RepeatMode: String, Codable, CaseIterable, Sendable {
    case off
    case all
    case one
}

struct Artist: Codable, Hashable, Identifiable, Sendable {
    let id: String
    let name: String
}

struct Artwork: Codable, Hashable, Sendable {
    let url: URL?
    let colors: [String]

    init(url: URL? = nil, colors: [String] = ["FF375F", "8E44EC"]) {
        self.url = url
        self.colors = colors
    }
}

struct Track: Codable, Hashable, Identifiable, Sendable {
    let id: String
    let title: String
    let artist: Artist
    let albumTitle: String
    let duration: TimeInterval
    let artwork: Artwork
    let isExplicit: Bool
    let downloadAllowed: Bool
    let availableQualities: Set<AudioQuality>

    init(
        id: String,
        title: String,
        artist: Artist,
        albumTitle: String,
        duration: TimeInterval,
        artwork: Artwork = Artwork(),
        isExplicit: Bool = false,
        downloadAllowed: Bool = true,
        availableQualities: Set<AudioQuality> = [.automatic, .high]
    ) {
        self.id = id
        self.title = title
        self.artist = artist
        self.albumTitle = albumTitle
        self.duration = duration
        self.artwork = artwork
        self.isExplicit = isExplicit
        self.downloadAllowed = downloadAllowed
        self.availableQualities = availableQualities
    }
}

struct Playlist: Codable, Hashable, Identifiable, Sendable {
    let id: String
    var name: String
    var description: String?
    var artwork: Artwork
    var tracks: [Track]
    var isEditable: Bool
    var totalTrackCount: Int? = nil
}

struct MusicShelf: Codable, Hashable, Identifiable, Sendable {
    enum Layout: String, Codable, Sendable {
        case cards
        case list
    }

    let id: String
    let title: String
    let subtitle: String?
    let layout: Layout
    let tracks: [Track]
}

struct HomeFeed: Codable, Hashable, Sendable {
    let greeting: String
    let featured: [Track]
    let shelves: [MusicShelf]
}

struct MusicLibrary: Codable, Hashable, Sendable {
    let recentlyAdded: [Track]
    let liked: [Track]
    let playlists: [Playlist]
}

struct PlaybackAsset: Codable, Hashable, Sendable {
    let url: URL
    let quality: AudioQuality
    let codec: String
    let bitDepth: Int?
    let sampleRate: Int?
    let expiresAt: Date?
    let allowsOfflineDownload: Bool
    var decryptionKey: String? = nil
    var transport: String? = nil
}

struct LyricsLine: Codable, Hashable, Identifiable, Sendable {
    let id: UUID
    let time: TimeInterval
    let text: String

    init(id: UUID = UUID(), time: TimeInterval, text: String) {
        self.id = id
        self.time = time
        self.text = text
    }
}

struct Lyrics: Codable, Hashable, Sendable {
    let trackID: String
    let writers: String?
    let lines: [LyricsLine]
}

struct UserProfile: Codable, Hashable, Sendable {
    let id: String
    let displayName: String
    let avatarURL: URL?
}

enum MusicServiceError: LocalizedError, Equatable {
    case notConfigured
    case unauthorized
    case forbidden
    case invalidResponse
    case http(Int)
    case offlineUnavailable
    case message(String)

    var errorDescription: String? {
        switch self {
        case .notConfigured: "A licensed music backend has not been configured."
        case .unauthorized: "Sign in to continue."
        case .forbidden: "This account is not entitled to this media."
        case .invalidResponse: "The music service returned an invalid response."
        case let .http(status): "The music service returned HTTP \(status)."
        case .offlineUnavailable: "This track is not licensed for offline playback."
        case let .message(message): message
        }
    }
}
