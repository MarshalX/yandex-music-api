import SwiftUI

struct AccountView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject private var settings: ProviderSettings
    @EnvironmentObject private var auth: AuthStore
    @EnvironmentObject private var player: PlayerStore
    @StateObject private var deviceLogin = YandexDeviceLogin()
    @State private var draft = ProviderConfiguration()
    @State private var token = ""
    @State private var message: String?
    @State private var isChecking = false

    var body: some View {
        NavigationStack {
            Form {
                Section("Music Provider") {
                    Picker("Provider", selection: $draft.kind) {
                        ForEach(ProviderKind.allCases) { Text($0.title).tag($0) }
                    }
                    .onChange(of: draft.kind) { _, kind in
                        if kind == .yandex { draft.endpoint = "https://api.music.yandex.net" }
                        if kind == .gateway { draft.endpoint = "" }
                    }
                    if draft.kind != .demo {
                        TextField("HTTPS API URL", text: $draft.endpoint)
                            .textInputAutocapitalization(.never).autocorrectionDisabled().keyboardType(.URL)
                    }
                    if draft.kind == .yandex {
                        Picker("Playback API", selection: $draft.streamAPI) {
                            ForEach(YandexMusicService.StreamAPI.allCases) { Text($0.title).tag($0) }
                        }
                    }
                    Button("Apply Provider") {
                        do {
                            if draft.kind != .demo { _ = try draft.validatedURL() }
                            player.stop()
                            try settings.apply(draft)
                            dismiss()
                        }
                        catch { message = error.localizedDescription }
                    }
                    .disabled(draft == settings.configuration)
                    Text("Credentials are stored separately for each API address. Changing the address does not copy a token to the new server.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
                if settings.configuration.kind != .demo {
                    Section("Account") {
                        if case let .signedIn(profile) = auth.state {
                            Label(profile.displayName, systemImage: "person.crop.circle.fill")
                            Button("Sign Out", role: .destructive) {
                                Task {
                                    player.stop()
                                    await auth.signOut()
                                    if auth.state == .signedOut { settings.reloadSession() }
                                }
                            }
                        } else {
                            if settings.configuration.kind == .yandex {
                                Button("Sign in with Yandex") {
                                    deviceLogin.start { value in
                                        if await auth.importToken(value) { settings.reloadSession() }
                                    }
                                }.disabled(deviceLogin.isRunning)
                                if let code = deviceLogin.userCode {
                                    Text(code).font(.title2.monospaced().bold()).textSelection(.enabled)
                                    if let url = deviceLogin.verificationURL { Link("Open Yandex and enter this code", destination: url) }
                                    HStack { ProgressView(); Text("Waiting for confirmation…") }
                                    Button("Cancel Login") { deviceLogin.cancel() }
                                }
                            }
                            DisclosureGroup("Sign in using an access token") {
                                SecureField("Access token", text: $token)
                                    .textInputAutocapitalization(.never).autocorrectionDisabled()
                                Button("Validate and Sign In") {
                                    isChecking = true
                                    Task {
                                        let value = token
                                        token = ""
                                        if await auth.importToken(value) { settings.reloadSession() }
                                        isChecking = false
                                    }
                                }.disabled(isChecking || token.isEmpty)
                            }
                        }
                        if let error = auth.errorMessage ?? deviceLogin.error {
                            Text(error).font(.footnote).foregroundStyle(.red)
                        }
                    }
                }
                Section("Audio Quality") {
                    Picker("Quality", selection: $player.preferredQuality) {
                        ForEach(AudioQuality.allCases) { Text($0.title).tag($0) }
                    }
                    Text("Lossless is requested from the provider. The player displays the returned codec; availability depends on the track and account.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
                Section("Privacy") {
                    Label("No analytics or advertising SDKs", systemImage: "hand.raised.fill")
                    Label("Credentials stored in Keychain", systemImage: "key.fill")
                    Text("Downloaded music and lyrics are isolated by provider and account and protected by iOS Data Protection.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Settings")
            .toolbar { ToolbarItem(placement: .confirmationAction) { Button("Done") { dismiss() } } }
            .onAppear { draft = settings.configuration }
            .onDisappear { deviceLogin.cancel(); token = "" }
            .alert("Settings", isPresented: Binding(get: { message != nil }, set: { if !$0 { message = nil } })) {
                Button("OK", role: .cancel) {}
            } message: { Text(message ?? "") }
        }
    }
}
