import Combine
import CryptoKit
import Foundation

@MainActor
final class AppContainer: ObservableObject {
    let service: AnyMusicService
    let offlineStore: OfflineStore
    let auth: AuthStore
    let catalog: CatalogStore
    let player: PlayerStore
    let downloads: DownloadsStore
    private let configuration: ProviderConfiguration

    init(configuration: ProviderConfiguration) {
        self.configuration = configuration
        let vault = KeychainTokenVault(account: configuration.credentialID)
        let token: @Sendable () async -> String? = {
            guard let value = try? await vault.load(), !value.isExpired else { return nil }
            return value.accessToken
        }
        let profile: @Sendable (String) async throws -> UserProfile
        switch configuration.kind {
        case .yandex:
            let url = (try? configuration.validatedURL()) ?? URL(string: "https://api.music.yandex.net")!
            let api = YandexMusicService(baseURL: url, streamAPI: configuration.streamAPI, token: token)
            service = AnyMusicService(api)
            let streamAPI = configuration.streamAPI
            profile = { value in
                try await YandexMusicService(baseURL: url, streamAPI: streamAPI, token: { value }).profile()
            }
        case .gateway:
            let url = (try? configuration.validatedURL()) ?? URL(string: "https://invalid.invalid")!
            service = AnyMusicService(BackendMusicService(baseURL: url, accessToken: token))
            profile = { value in
                try await BackendMusicService(baseURL: url, accessToken: { value }).profile()
            }
        case .demo:
            service = AnyMusicService(DemoMusicService())
            profile = { _ in UserProfile(id: "demo", displayName: "Local Demo", avatarURL: nil) }
        }
        auth = AuthStore(configuration: configuration, vault: vault, profileLoader: profile)
        offlineStore = OfflineStore()
        catalog = CatalogStore(service: service)
        player = PlayerStore(service: service, offlineStore: offlineStore)
        downloads = DownloadsStore(offlineStore: offlineStore, service: service)
    }

    func bootstrap() async {
        await auth.restore()
        let account: String
        if case let .signedIn(profile) = auth.state { account = profile.id }
        else { account = configuration.kind == .demo ? "demo" : "signed-out" }
        let scope = configuration.credentialID + ":" + account
        await offlineStore.setScope(scope)
        await downloads.refresh()
        if configuration.kind == .demo || account != "signed-out" { await catalog.bootstrap() }
    }
}
