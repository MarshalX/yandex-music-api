import AuthenticationServices
import Foundation
import UIKit

enum AuthError: LocalizedError, Equatable {
    case notConfigured
    case invalidAuthorizationURL
    case canceled
    case invalidCallback
    case stateMismatch
    case tokenExchangeFailed(Int)
    case invalidTokenResponse
    case profileFailed(Int)
    case keychain(OSStatus)
    case randomGenerationFailed(OSStatus)

    var errorDescription: String? {
        switch self {
        case .notConfigured: "Add your registered Yandex OAuth Client ID in Config/Local.xcconfig."
        case .invalidAuthorizationURL: "Could not create the authorization URL."
        case .canceled: "Sign in was canceled."
        case .invalidCallback: "Yandex returned an invalid authorization callback."
        case .stateMismatch: "The authorization response could not be verified."
        case let .tokenExchangeFailed(code): "Token exchange failed with HTTP \(code)."
        case .invalidTokenResponse: "Yandex returned an invalid token response."
        case let .profileFailed(code): "Profile request failed with HTTP \(code)."
        case let .keychain(status): "Keychain error \(status)."
        case let .randomGenerationFailed(status): "Secure random generator error \(status)."
        }
    }
}

@MainActor
final class YandexOAuthClient: NSObject, ASWebAuthenticationPresentationContextProviding {
    private struct TokenResponse: Decodable {
        let accessToken: String
        let tokenType: String?
        let refreshToken: String?
        let expiresIn: TimeInterval?

        enum CodingKeys: String, CodingKey {
            case accessToken = "access_token"
            case tokenType = "token_type"
            case refreshToken = "refresh_token"
            case expiresIn = "expires_in"
        }
    }

    private struct ProfileResponse: Decodable {
        let id: String
        let displayName: String?
        let realName: String?
        let login: String?
        let defaultAvatarID: String?

        enum CodingKeys: String, CodingKey {
            case id
            case displayName = "display_name"
            case realName = "real_name"
            case login
            case defaultAvatarID = "default_avatar_id"
        }
    }

    private let clientID: String
    private let redirectURI: String
    private let session: URLSession
    private var webSession: ASWebAuthenticationSession?

    init(bundle: Bundle = .main, session: URLSession = .shared) {
        clientID = (bundle.object(forInfoDictionaryKey: "YandexClientID") as? String) ?? ""
        redirectURI = (bundle.object(forInfoDictionaryKey: "YandexRedirectURI") as? String) ?? "maplemusic://oauth"
        self.session = session
    }

    var isConfigured: Bool {
        !clientID.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
            && clientID != "$(YANDEX_CLIENT_ID)"
    }

    func authorize() async throws -> (OAuthToken, UserProfile) {
        guard isConfigured else { throw AuthError.notConfigured }
        let pkce = try PKCE.make()
        let expectedState = try PKCE.state()
        let callback = try await authorizationCallback(pkce: pkce, state: expectedState)
        let components = URLComponents(url: callback, resolvingAgainstBaseURL: false)
        guard components?.queryItems?.first(where: { $0.name == "state" })?.value == expectedState else {
            throw AuthError.stateMismatch
        }
        guard let code = components?.queryItems?.first(where: { $0.name == "code" })?.value, !code.isEmpty else {
            throw AuthError.invalidCallback
        }
        let token = try await exchange(code: code, verifier: pkce.verifier)
        let profile = try await fetchProfile(accessToken: token.accessToken)
        return (token, profile)
    }

    func fetchProfile(accessToken: String) async throws -> UserProfile {
        var components = URLComponents(string: "https://login.yandex.ru/info")
        components?.queryItems = [URLQueryItem(name: "format", value: "json")]
        guard let url = components?.url else { throw AuthError.invalidAuthorizationURL }
        var request = URLRequest(url: url)
        request.setValue("OAuth \(accessToken)", forHTTPHeaderField: "Authorization")
        let (data, response) = try await session.data(for: request)
        guard let http = response as? HTTPURLResponse else { throw AuthError.invalidTokenResponse }
        guard (200 ..< 300).contains(http.statusCode) else { throw AuthError.profileFailed(http.statusCode) }
        let profile = try JSONDecoder().decode(ProfileResponse.self, from: data)
        let avatarURL = profile.defaultAvatarID.flatMap {
            URL(string: "https://avatars.yandex.net/get-yapic/\($0)/islands-200")
        }
        return UserProfile(
            id: profile.id,
            displayName: profile.displayName ?? profile.realName ?? profile.login ?? "Yandex user",
            avatarURL: avatarURL
        )
    }

    func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
        let scenes = UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }
        if let window = scenes.flatMap(\.windows).first(where: \.isKeyWindow) {
            return window
        }
        if let scene = scenes.first, let window = scene.windows.first {
            return window
        }
        return ASPresentationAnchor()
    }

    private func authorizationCallback(pkce: PKCEPair, state: String) async throws -> URL {
        var components = URLComponents(string: "https://oauth.yandex.com/authorize")
        components?.queryItems = [
            URLQueryItem(name: "response_type", value: "code"),
            URLQueryItem(name: "client_id", value: clientID),
            URLQueryItem(name: "redirect_uri", value: redirectURI),
            URLQueryItem(name: "scope", value: "login:info"),
            URLQueryItem(name: "state", value: state),
            URLQueryItem(name: "code_challenge", value: pkce.challenge),
            URLQueryItem(name: "code_challenge_method", value: "S256"),
            URLQueryItem(name: "force_confirm", value: "yes"),
        ]
        guard let url = components?.url, let callbackScheme = URL(string: redirectURI)?.scheme else {
            throw AuthError.invalidAuthorizationURL
        }
        return try await withCheckedThrowingContinuation { continuation in
            let session = ASWebAuthenticationSession(url: url, callbackURLScheme: callbackScheme) { [weak self] callback, error in
                Task { @MainActor in
                    self?.webSession = nil
                    if let authenticationError = error as? ASWebAuthenticationSessionError,
                       authenticationError.code == .canceledLogin
                    {
                        continuation.resume(throwing: AuthError.canceled)
                    } else if let error {
                        continuation.resume(throwing: error)
                    } else if let callback {
                        continuation.resume(returning: callback)
                    } else {
                        continuation.resume(throwing: AuthError.invalidCallback)
                    }
                }
            }
            session.presentationContextProvider = self
            session.prefersEphemeralWebBrowserSession = false
            webSession = session
            if !session.start() {
                webSession = nil
                continuation.resume(throwing: AuthError.invalidAuthorizationURL)
            }
        }
    }

    private func exchange(code: String, verifier: String) async throws -> OAuthToken {
        guard let url = URL(string: "https://oauth.yandex.com/token") else {
            throw AuthError.invalidAuthorizationURL
        }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        request.httpBody = formEncoded([
            "grant_type": "authorization_code",
            "code": code,
            "client_id": clientID,
            "redirect_uri": redirectURI,
            "code_verifier": verifier,
        ])
        let (data, response) = try await session.data(for: request)
        guard let http = response as? HTTPURLResponse else { throw AuthError.invalidTokenResponse }
        guard (200 ..< 300).contains(http.statusCode) else { throw AuthError.tokenExchangeFailed(http.statusCode) }
        guard let decoded = try? JSONDecoder().decode(TokenResponse.self, from: data) else {
            throw AuthError.invalidTokenResponse
        }
        return OAuthToken(
            accessToken: decoded.accessToken,
            tokenType: decoded.tokenType ?? "bearer",
            refreshToken: decoded.refreshToken,
            expiresAt: decoded.expiresIn.map { Date().addingTimeInterval($0) }
        )
    }

    private func formEncoded(_ fields: [String: String]) -> Data {
        let allowed = CharacterSet.alphanumerics.union(CharacterSet(charactersIn: "-._~"))
        let value = fields.sorted { $0.key < $1.key }.map { key, value in
            let encodedKey = key.addingPercentEncoding(withAllowedCharacters: allowed) ?? key
            let encodedValue = value.addingPercentEncoding(withAllowedCharacters: allowed) ?? value
            return "\(encodedKey)=\(encodedValue)"
        }.joined(separator: "&")
        return Data(value.utf8)
    }
}
