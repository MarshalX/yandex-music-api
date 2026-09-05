import Combine
import Foundation

@MainActor
final class YandexDeviceLogin: ObservableObject {
    @Published private(set) var userCode: String?
    @Published private(set) var verificationURL: URL?
    @Published private(set) var isRunning = false
    @Published var error: String?
    private var task: Task<Void, Never>?
    // Public device-client parameters used by yandex-music-api; server acceptance
    // can change. An account token can also be entered directly in Settings.
    private let clientID = "23cabbbdc6cd418abb4b39c32c41195d"
    private let clientSecret = "53bc75238f0c4d08a118e51fe9203300"

    func start(receive: @escaping @MainActor (String) async -> Void) {
        cancel()
        isRunning = true
        error = nil
        task = Task {
            defer { isRunning = false }
            do {
                let code = try await post("device/code", fields: ["client_id": clientID,
                    "device_id": UUID().uuidString, "device_name": "Maple Music"])
                guard let deviceCode = code["device_code"].string, let userCode = code["user_code"].string,
                      let raw = code["verification_url"].string ?? code["verification_uri"].string,
                      let url = URL(string: raw), url.scheme == "https",
                      ["oauth.yandex.ru", "oauth.yandex.com", "ya.ru", "passport.yandex.ru"].contains(url.host ?? "") else {
                    throw MusicServiceError.message("Device login is unavailable. Use an account token in Settings.")
                }
                self.userCode = userCode
                self.verificationURL = url
                let deadline = Date().addingTimeInterval(code["expires_in"].number ?? 600)
                var interval = max(code["interval"].number ?? 5, 5)
                while Date() < deadline {
                    try await Task.sleep(for: .seconds(interval))
                    let result = try await post("token", fields: ["grant_type": "device_code", "code": deviceCode,
                        "client_id": clientID, "client_secret": clientSecret])
                    try Task.checkCancellation()
                    if let token = result["access_token"].string {
                        await receive(token)
                        return
                    }
                    switch result["error"].string {
                    case "authorization_pending": continue
                    case "slow_down": interval += 5
                    default: throw MusicServiceError.message("Login was declined or expired. Request a new code.")
                    }
                }
                throw MusicServiceError.message("The login code expired.")
            } catch is CancellationError { }
            catch { self.error = error.localizedDescription }
        }
    }
    func cancel() {
        task?.cancel()
        task = nil
        isRunning = false
        userCode = nil
        verificationURL = nil
    }
    private func post(_ path: String, fields: [String: String]) async throws -> YandexJSON {
        var request = URLRequest(url: URL(string: "https://oauth.yandex.ru/\(path)")!)
        request.httpMethod = "POST"
        request.timeoutInterval = 30
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        let allowed = CharacterSet.alphanumerics.union(CharacterSet(charactersIn: "-._~"))
        request.httpBody = Data(fields.sorted { $0.key < $1.key }.map {
            "\($0.key.addingPercentEncoding(withAllowedCharacters: allowed)!)=\($0.value.addingPercentEncoding(withAllowedCharacters: allowed)!)"
        }.joined(separator: "&").utf8)
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse, http.statusCode == 200 || http.statusCode == 400 else {
            throw MusicServiceError.message("The authorization server is unavailable.")
        }
        return try JSONDecoder().decode(YandexJSON.self, from: data)
    }
}
