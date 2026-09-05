import CryptoKit
import Foundation

actor YandexMusicService: MusicService {
    enum StreamAPI: String, Codable, CaseIterable, Identifiable {
        case modern, legacy
        var id: String { rawValue }
        var title: String { self == .modern ? "File info · Lossless / encraw" : "Download info · MP3 / AAC" }
    }

    private let baseURL: URL
    private let token: @Sendable () async -> String?
    private let session: URLSession
    private let streamAPI: StreamAPI
    private static let signatureKey = "p93jhgh689SBReK6ghtw62"

    init(baseURL: URL = URL(string: "https://api.music.yandex.net")!, streamAPI: StreamAPI = .modern,
         session: URLSession = .shared, token: @escaping @Sendable () async -> String?) {
        self.baseURL = baseURL; self.streamAPI = streamAPI; self.session = session; self.token = token
    }

    func profile() async throws -> UserProfile {
        let result = try await request("account/status")
        let account = result["account"]
        guard let id = account["uid"].string, id != "0" else { throw MusicServiceError.unauthorized }
        return UserProfile(id: id, displayName: account["displayName"].string ?? account["login"].string ?? "Yandex Music", avatarURL: nil)
    }

    func home() async throws -> HomeFeed {
        let result = try await request("rotor/station/user:onyourwave/tracks", query: ["settings2": "true"])
        let tracks = result["sequence"].array.compactMap { $0["track"].track() }
        return HomeFeed(greeting: "Listen Now", featured: Array(tracks.prefix(5)), shelves: [
            MusicShelf(id: "my-wave", title: "My Wave", subtitle: "For you", layout: .list, tracks: tracks)
        ])
    }

    func search(query: String) async throws -> [Track] {
        let result = try await request("search", query: ["text": query, "type": "track", "page": "0", "nocorrect": "false"])
        return result["tracks"]["results"].array.compactMap { $0.track() }
    }

    func library() async throws -> MusicLibrary {
        let uid = try await profile().id
        let likedResult = try await request("users/\(uid)/likes/tracks")
        let short = likedResult["library"]["tracks"].array
        let ids = short.compactMap { item -> String? in
            guard let id = item["id"].string else { return nil }
            return item["albumId"].string.map { "\(id):\($0)" } ?? id
        }
        let liked = try await fetchTracks(ids)
        let result = try await request("users/\(uid)/playlists/list")
        let playlists = result.array.compactMap { playlistModel($0, currentUID: uid) }
        return MusicLibrary(recentlyAdded: Array(liked.prefix(30)), liked: liked, playlists: playlists)
    }

    func playlist(id: String) async throws -> Playlist {
        let uid = try await profile().id
        let result = try await playlistJSON(id)
        guard var playlist = playlistModel(result, currentUID: uid) else { throw MusicServiceError.invalidResponse }
        let shorts = result["tracks"].array
        // Hydrate short responses; preserve the server's order.
        let ids = shorts.compactMap { item -> String? in
            if let track = item["track"].track() { return track.id }
            guard let id = item["id"].string else { return nil }
            return item["albumId"].string.map { "\(id):\($0)" } ?? id
        }
        playlist.tracks = try await fetchTracks(ids)
        return playlist
    }

    func createPlaylist(name: String) async throws -> Playlist {
        let uid = try await profile().id
        let result = try await request("users/\(uid)/playlists/create", form: ["title": name, "visibility": "private"])
        guard let playlist = playlistModel(result, currentUID: uid) else { throw MusicServiceError.invalidResponse }
        return playlist
    }

    func add(trackID: String, toPlaylistID playlistID: String) async throws {
        let parts = try components(playlistID)
        let uid = try await profile().id
        guard parts[0] == uid else { throw MusicServiceError.forbidden }
        let playlist = try await playlistJSON(playlistID)
        let tracks = try await fetchTracks([trackID])
        guard let track = tracks.first else { throw MusicServiceError.http(404) }
        let trackParts = track.id.split(separator: ":").map(String.init)
        guard trackParts.count == 2 else { throw MusicServiceError.message("This track has no album identifier.") }
        let operation: [[String: Any]] = [["op": "insert", "at": Int(playlist["trackCount"].number ?? 0),
                                          "tracks": [["id": trackParts[0], "albumId": trackParts[1]]]]]
        try await changePlaylist(parts: parts, revision: playlist["revision"].string, operations: operation)
    }

    func remove(trackID: String, fromPlaylistID playlistID: String) async throws {
        let parts = try components(playlistID)
        let uid = try await profile().id
        guard parts[0] == uid else { throw MusicServiceError.forbidden }
        let playlist = try await playlistJSON(playlistID)
        let baseID = trackID.split(separator: ":").first.map(String.init)
        guard let index = playlist["tracks"].array.firstIndex(where: { ($0["id"].string ?? $0["track"]["id"].string) == baseID }) else { return }
        try await changePlaylist(parts: parts, revision: playlist["revision"].string,
                                 operations: [["op": "delete", "from": index, "to": index + 1]])
    }

    func setFavorite(trackID: String, isFavorite: Bool) async throws {
        let uid = try await profile().id
        _ = try await request("users/\(uid)/likes/tracks/\(isFavorite ? "add-multiple" : "remove")", form: ["track-ids": trackID])
    }

    func playbackAsset(for track: Track, quality: AudioQuality) async throws -> PlaybackAsset {
        let id = try trackIdentifier(track.id)
        if streamAPI == .legacy { return try await legacyAsset(id: id, track: track, quality: quality) }
        let timestamp = String(Int(Date().timeIntervalSince1970))
        let requested = quality == .lossless ? "lossless" : "nq"
        let codecs = "flac,aac,he-aac,mp3"
        let transport = "encraw"
        let sign = Self.sign(timestamp + id + requested + codecs.replacingOccurrences(of: ",", with: "") + transport)
            .replacingOccurrences(of: "=", with: "")
        let result = try await request("get-file-info", query: ["ts": timestamp, "trackId": id, "quality": requested,
            "codecs": codecs, "transports": transport, "sign": sign])
        let info = result["downloadInfo"]
        guard let address = info["url"].string ?? info["urls"].array.first?.string,
              let url = URL(string: address), url.scheme == "https", let codec = info["codec"].string else {
            throw MusicServiceError.invalidResponse
        }
        guard info["preview"].bool != true else { throw MusicServiceError.forbidden }
        let isLossless = codec == "flac" || codec == "flac-mp4" || codec == "alac"
        if quality == .lossless && !isLossless { throw MusicServiceError.message("Lossless is unavailable for this track or account. Select High Quality to continue.") }
        let key = info["key"].string
        if info["transport"].string == "encraw", key == nil { throw MusicServiceError.invalidResponse }
        return PlaybackAsset(url: url, quality: isLossless ? .lossless : .high, codec: codec,
            bitDepth: info["bitDepth"].number.map(Int.init), sampleRate: info["sampleRate"].number.map(Int.init),
            expiresAt: nil, allowsOfflineDownload: track.downloadAllowed, decryptionKey: key, transport: info["transport"].string)
    }

    func lyrics(for track: Track) async throws -> Lyrics? {
        let id = try trackIdentifier(track.id)
        let timestamp = String(Int(Date().timeIntervalSince1970))
        do {
            let result = try await request("tracks/\(id)/lyrics", query: ["format": "LRC", "timeStamp": timestamp,
                "sign": Self.sign(id + timestamp)])
            guard let raw = result["downloadUrl"].string, let url = URL(string: raw), url.scheme == "https" else { return nil }
            let (data, response) = try await session.data(from: url)
            try Self.validate(response)
            guard let text = String(data: data, encoding: .utf8) else { throw MusicServiceError.invalidResponse }
            return Lyrics(trackID: track.id, writers: result["writers"].array.compactMap(\.string).joined(separator: ", "), lines: LRCParser.parse(text))
        } catch MusicServiceError.http(404) { return nil }
    }

    private func legacyAsset(id: String, track: Track, quality: AudioQuality) async throws -> PlaybackAsset {
        if quality == .lossless { throw MusicServiceError.message("Lossless requires the File info API. Change the API in Settings.") }
        let result = try await request("tracks/\(id)/download-info")
        guard let info = result.array.filter({ $0["preview"].bool == false && $0["codec"].string == "mp3" })
            .max(by: { ($0["bitrateInKbps"].number ?? 0) < ($1["bitrateInKbps"].number ?? 0) }),
              let raw = info["downloadInfoUrl"].string, let descriptor = URL(string: raw), descriptor.scheme == "https"
        else { throw MusicServiceError.forbidden }
        var url = descriptor
        if info["direct"].bool != true {
            var components = URLComponents(url: descriptor, resolvingAgainstBaseURL: false)!
            components.queryItems = (components.queryItems ?? []) + [URLQueryItem(name: "format", value: "json")]
            let (data, response) = try await session.data(from: components.url!)
            try Self.validate(response)
            let details = try JSONDecoder().decode(YandexJSON.self, from: data)
            guard let host = details["host"].string, let path = details["path"].string, path.hasPrefix("/"),
                  let timestamp = details["ts"].string, let salt = details["s"].string else { throw MusicServiceError.invalidResponse }
            let digest = Insecure.MD5.hash(data: Data(("XGRlBW9FXlekgbPrRHuSiA" + path.dropFirst() + salt).utf8))
                .map { String(format: "%02x", $0) }.joined()
            guard let resolved = URL(string: "https://\(host)/get-mp3/\(digest)/\(timestamp)\(path)") else { throw MusicServiceError.invalidResponse }
            url = resolved
        }
        return PlaybackAsset(url: url, quality: .high, codec: "mp3", bitDepth: nil, sampleRate: nil, expiresAt: nil,
                             allowsOfflineDownload: track.downloadAllowed, transport: info["container"].string)
    }

    private func fetchTracks(_ ids: [String]) async throws -> [Track] {
        var tracks: [Track] = []
        for start in stride(from: 0, to: ids.count, by: 100) {
            try Task.checkCancellation()
            let batch = Array(ids[start..<min(start + 100, ids.count)])
            let result = try await request("tracks", form: ["track-ids": batch.joined(separator: ","), "with-positions": "true"])
            tracks += result.array.compactMap { $0.track() }
        }
        return tracks
    }

    private func playlistModel(_ value: YandexJSON, currentUID: String) -> Playlist? {
        guard let kind = value["kind"].string, let title = value["title"].string else { return nil }
        let owner = value["owner"]["uid"].string ?? currentUID
        let cover = value["cover"]["uri"].string ?? value["cover"]["itemsUri"].array.first?.string
        return Playlist(id: "\(owner):\(kind)", name: title, description: value["description"].string,
            artwork: Artwork(url: YandexJSON.artworkURL(cover)), tracks: value["tracks"].array.compactMap { $0["track"].track() },
            isEditable: owner == currentUID, totalTrackCount: value["trackCount"].number.map(Int.init))
    }

    private func playlistJSON(_ id: String) async throws -> YandexJSON {
        let parts = try components(id)
        return try await request("users/\(parts[0])/playlists/\(parts[1])")
    }
    private func components(_ id: String) throws -> [String] {
        let parts = id.split(separator: ":").map(String.init)
        guard parts.count == 2, parts.allSatisfy({ !$0.isEmpty && $0.allSatisfy(\.isNumber) }) else { throw MusicServiceError.invalidResponse }
        return parts
    }
    private func trackIdentifier(_ id: String) throws -> String {
        guard let value = id.split(separator: ":").first, !value.isEmpty, value.allSatisfy(\.isNumber) else { throw MusicServiceError.invalidResponse }
        return String(value)
    }
    private func changePlaylist(parts: [String], revision: String?, operations: [[String: Any]]) async throws {
        guard let revision else { throw MusicServiceError.invalidResponse }
        let data = try JSONSerialization.data(withJSONObject: operations, options: [.sortedKeys])
        _ = try await request("users/\(parts[0])/playlists/\(parts[1])/change", form: ["kind": parts[1], "revision": revision, "diff": String(decoding: data, as: UTF8.self)])
    }
    static func sign(_ message: String) -> String {
        Data(HMAC<SHA256>.authenticationCode(for: Data(message.utf8), using: SymmetricKey(data: Data(signatureKey.utf8)))).base64EncodedString()
    }
    private func request(_ path: String, query: [String: String] = [:], form: [String: String]? = nil) async throws -> YandexJSON {
        guard let token = await token(), !token.isEmpty else { throw MusicServiceError.unauthorized }
        var components = URLComponents(url: baseURL.appending(path: path), resolvingAgainstBaseURL: false)!
        components.queryItems = query.sorted { $0.key < $1.key }.map { URLQueryItem(name: $0.key, value: $0.value) }
        guard let url = components.url, url.scheme == "https" else { throw MusicServiceError.notConfigured }
        var request = URLRequest(url: url)
        request.timeoutInterval = 30
        request.setValue("OAuth \(token)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue("MapleMusic/0.2", forHTTPHeaderField: "User-Agent")
        if let form {
            request.httpMethod = "POST"
            request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
            let allowed = CharacterSet.alphanumerics.union(CharacterSet(charactersIn: "-._~"))
            request.httpBody = Data(form.sorted { $0.key < $1.key }.map { key, value in
                "\(key.addingPercentEncoding(withAllowedCharacters: allowed)!)=\(value.addingPercentEncoding(withAllowedCharacters: allowed)!)"
            }.joined(separator: "&").utf8)
        }
        let (data, response) = try await session.data(for: request)
        try Self.validate(response)
        let decoded = try JSONDecoder().decode(YandexJSON.self, from: data)
        if decoded["error"]["name"].string != nil { throw MusicServiceError.invalidResponse }
        return decoded["result"]
    }
    private static func validate(_ response: URLResponse) throws {
        guard let http = response as? HTTPURLResponse else { throw MusicServiceError.invalidResponse }
        switch http.statusCode {
        case 200..<300: return
        case 401: throw MusicServiceError.unauthorized
        case 403: throw MusicServiceError.forbidden
        case 451: throw MusicServiceError.message("The provider is unavailable in this region (HTTP 451).")
        default: throw MusicServiceError.http(http.statusCode)
        }
    }
}
