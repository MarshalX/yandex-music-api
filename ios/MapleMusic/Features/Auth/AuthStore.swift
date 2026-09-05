import Combine
import Foundation

@MainActor
final class AuthStore: ObservableObject {
    enum State: Equatable {
        case signedOut, restoring, signingIn
        case signedIn(UserProfile)
    }
    @Published private(set) var state: State = .restoring
    @Published var errorMessage: String?
    private let configuration: ProviderConfiguration
    private let vault: KeychainTokenVault
    private let profileLoader: @Sendable (String) async throws -> UserProfile
    private let cacheKey: String

    init(configuration: ProviderConfiguration, vault: KeychainTokenVault,
         profileLoader: @escaping @Sendable (String) async throws -> UserProfile) {
        self.configuration = configuration; self.vault = vault; self.profileLoader = profileLoader
        cacheKey = "profile-" + configuration.credentialID
    }
    var isConfigured: Bool { configuration.kind != .demo }
    var usesMusicBackend: Bool { configuration.kind == .gateway }

    func restore() async {
        state = .restoring
        guard configuration.kind != .demo else { state = .signedOut; return }
        do {
            guard let token = try await vault.load(), !token.isExpired else { state = .signedOut; return }
            do {
                let profile = try await profileLoader(token.accessToken)
                cache(profile)
                state = .signedIn(profile)
            } catch let error as URLError where [.notConnectedToInternet, .networkConnectionLost, .timedOut, .cannotFindHost, .cannotConnectToHost].contains(error.code) {
                if let data = UserDefaults.standard.data(forKey: cacheKey), let profile = try? JSONDecoder().decode(UserProfile.self, from: data) {
                    state = .signedIn(profile)
                } else { state = .signedOut }
            }
        } catch {
            state = .signedOut
            errorMessage = error.localizedDescription
        }
    }

    // Token import is validated against the chosen provider before it is stored.
    // A Yandex ID login:info token alone does not confer Music API access.
    func importToken(_ raw: String) async -> Bool {
        let token = raw.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !token.isEmpty else { errorMessage = "Enter an access token."; return false }
        state = .signingIn
        do {
            let profile = try await profileLoader(token)
            try await vault.save(OAuthToken(accessToken: token, tokenType: "OAuth", refreshToken: nil, expiresAt: nil))
            cache(profile)
            state = .signedIn(profile)
            errorMessage = nil
            return true
        } catch {
            state = .signedOut
            errorMessage = error.localizedDescription
            return false
        }
    }

    func signOut() async {
        do { try await vault.clear() }
        catch { errorMessage = error.localizedDescription; return }
        UserDefaults.standard.removeObject(forKey: cacheKey)
        state = .signedOut
    }
    private func cache(_ profile: UserProfile) {
        if let data = try? JSONEncoder().encode(profile) { UserDefaults.standard.set(data, forKey: cacheKey) }
    }
}
