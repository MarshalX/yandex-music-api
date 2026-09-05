import Foundation

actor BackendMusicService: MusicService {
    private let baseURL: URL
    private let session: URLSession
    private let accessToken: @Sendable () async -> String?
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder

    init(
        baseURL: URL,
        session: URLSession = .shared,
        accessToken: @escaping @Sendable () async -> String? = { nil }
    ) {
        self.baseURL = baseURL
        self.session = session
        self.accessToken = accessToken
        decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
    }

    func home() async throws -> HomeFeed {
        try await request(path: "/v1/home")
    }

    func profile() async throws -> UserProfile { try await request(path: "/v1/me") }

    func search(query: String) async throws -> [Track] {
        try await request(path: "/v1/search", query: [URLQueryItem(name: "q", value: query)])
    }

    func library() async throws -> MusicLibrary {
        try await request(path: "/v1/library")
    }

    func playlist(id: String) async throws -> Playlist {
        try await request(path: "/v1/playlists/\(escaped(id))")
    }

    func createPlaylist(name: String) async throws -> Playlist {
        try await request(path: "/v1/playlists", method: "POST", body: ["name": name])
    }

    func add(trackID: String, toPlaylistID playlistID: String) async throws {
        try await requestWithoutBody(path: "/v1/playlists/\(escaped(playlistID))/tracks/\(escaped(trackID))", method: "PUT")
    }

    func remove(trackID: String, fromPlaylistID playlistID: String) async throws {
        try await requestWithoutBody(path: "/v1/playlists/\(escaped(playlistID))/tracks/\(escaped(trackID))", method: "DELETE")
    }

    func setFavorite(trackID: String, isFavorite: Bool) async throws {
        try await requestWithoutBody(
            path: "/v1/library/favorites/\(escaped(trackID))",
            method: isFavorite ? "PUT" : "DELETE"
        )
    }

    func playbackAsset(for track: Track, quality: AudioQuality) async throws -> PlaybackAsset {
        try await request(
            path: "/v1/tracks/\(escaped(track.id))/playback",
            query: [URLQueryItem(name: "quality", value: quality.rawValue)]
        )
    }

    func lyrics(for track: Track) async throws -> Lyrics? {
        do {
            return try await request(path: "/v1/tracks/\(escaped(track.id))/lyrics")
        } catch MusicServiceError.http(404) {
            return nil
        }
    }

    private func escaped(_ component: String) -> String {
        component.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? component
    }

    private func makeRequest(path: String, query: [URLQueryItem], method: String) async throws -> URLRequest {
        guard var components = URLComponents(url: baseURL.appending(path: path), resolvingAgainstBaseURL: false) else {
            throw MusicServiceError.invalidResponse
        }
        components.queryItems = query.isEmpty ? nil : query
        guard let url = components.url, url.scheme?.lowercased() == "https" else {
            throw MusicServiceError.notConfigured
        }
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.timeoutInterval = 30
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        if let token = await accessToken(), !token.isEmpty {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        return request
    }

    private func request<Response: Decodable, Body: Encodable>(
        path: String,
        query: [URLQueryItem] = [],
        method: String = "GET",
        body: Body
    ) async throws -> Response {
        var request = try await makeRequest(path: path, query: query, method: method)
        request.httpBody = try encoder.encode(body)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        return try await execute(request)
    }

    private func request<Response: Decodable>(
        path: String,
        query: [URLQueryItem] = [],
        method: String = "GET"
    ) async throws -> Response {
        let request = try await makeRequest(path: path, query: query, method: method)
        return try await execute(request)
    }

    private func requestWithoutBody(path: String, method: String) async throws {
        let request = try await makeRequest(path: path, query: [], method: method)
        let (_, response) = try await session.data(for: request)
        try validate(response)
    }

    private func execute<Response: Decodable>(_ request: URLRequest) async throws -> Response {
        let (data, response) = try await session.data(for: request)
        try validate(response)
        do {
            return try decoder.decode(Response.self, from: data)
        } catch {
            throw MusicServiceError.invalidResponse
        }
    }

    private func validate(_ response: URLResponse) throws {
        guard let http = response as? HTTPURLResponse else {
            throw MusicServiceError.invalidResponse
        }
        switch http.statusCode {
        case 200 ..< 300: return
        case 401: throw MusicServiceError.unauthorized
        case 403: throw MusicServiceError.forbidden
        default: throw MusicServiceError.http(http.statusCode)
        }
    }
}
