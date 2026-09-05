import SwiftUI

@main
struct MapleMusicApp: App {
    @StateObject private var settings = ProviderSettings()

    var body: some Scene {
        WindowGroup {
            ProviderRoot(configuration: settings.configuration)
                .id(settings.generation)
                .environmentObject(settings)
        }
    }
}

private struct ProviderRoot: View {
    @StateObject private var container: AppContainer
    init(configuration: ProviderConfiguration) {
        _container = StateObject(wrappedValue: AppContainer(configuration: configuration))
    }
    var body: some View {
            RootView()
                .environmentObject(container)
                .environmentObject(container.auth)
                .environmentObject(container.catalog)
                .environmentObject(container.player)
                .environmentObject(container.downloads)
                .task { await container.bootstrap() }
                .tint(.mapleAccent)
                .onDisappear { container.player.stop() }
    }
}
