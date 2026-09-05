import SwiftUI

extension Color {
    static let mapleAccent = Color(red: 0.98, green: 0.12, blue: 0.29)
    static let mapleSecondary = Color(red: 0.58, green: 0.22, blue: 0.92)

    init(hex: String) {
        let cleaned = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var value: UInt64 = 0
        Scanner(string: cleaned).scanHexInt64(&value)
        switch cleaned.count {
        case 6:
            self.init(
                red: Double((value >> 16) & 0xFF) / 255,
                green: Double((value >> 8) & 0xFF) / 255,
                blue: Double(value & 0xFF) / 255
            )
        case 8:
            self.init(
                red: Double((value >> 24) & 0xFF) / 255,
                green: Double((value >> 16) & 0xFF) / 255,
                blue: Double((value >> 8) & 0xFF) / 255,
                opacity: Double(value & 0xFF) / 255
            )
        default:
            self = .mapleAccent
        }
    }
}

extension TimeInterval {
    var musicTime: String {
        guard isFinite, self >= 0 else { return "0:00" }
        let total = Int(self.rounded(.down))
        return String(format: "%d:%02d", total / 60, total % 60)
    }
}

struct ArtworkView: View {
    let artwork: Artwork
    var cornerRadius: CGFloat = 12

    var body: some View {
        ZStack {
            LinearGradient(colors: colors, startPoint: .topLeading, endPoint: .bottomTrailing)
            if let url = artwork.url {
                AsyncImage(url: url) { phase in
                    if case let .success(image) = phase {
                        image.resizable().scaledToFill()
                    } else {
                        placeholder
                    }
                }
            } else {
                placeholder
            }
        }
        .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                .strokeBorder(.white.opacity(0.12), lineWidth: 0.5)
        }
        .accessibilityHidden(true)
    }

    private var colors: [Color] {
        let values = artwork.colors.map(Color.init(hex:))
        return values.isEmpty ? [.mapleAccent, .mapleSecondary] : values
    }

    private var placeholder: some View {
        Image(systemName: "waveform")
            .font(.system(size: 36, weight: .medium))
            .foregroundStyle(.white.opacity(0.9))
    }
}

struct TrackRow: View {
    let track: Track
    let isDownloaded: Bool
    let isDownloading: Bool
    let play: () -> Void
    let toggleDownload: () -> Void

    var body: some View {
        HStack(spacing: 12) {
            Button(action: play) {
                ArtworkView(artwork: track.artwork, cornerRadius: 7)
                    .frame(width: 52, height: 52)
                    .overlay {
                        Image(systemName: "play.fill")
                            .font(.caption.bold())
                            .foregroundStyle(.white)
                            .shadow(radius: 4)
                    }
            }
            .buttonStyle(.plain)

            VStack(alignment: .leading, spacing: 3) {
                HStack(spacing: 5) {
                    Text(track.title).lineLimit(1)
                    if track.isExplicit {
                        Image(systemName: "e.square.fill").font(.caption2).foregroundStyle(.secondary)
                    }
                }
                .font(.body)
                Text("\(track.artist.name) · \(track.albumTitle)")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
            }
            Spacer(minLength: 8)
            if isDownloading {
                ProgressView().controlSize(.small)
            } else {
                Button(action: toggleDownload) {
                    Image(systemName: isDownloaded ? "arrow.down.circle.fill" : "arrow.down.circle")
                        .font(.title3)
                        .foregroundStyle(isDownloaded ? Color.mapleAccent : .secondary)
                }
                .buttonStyle(.plain)
                .disabled(!track.downloadAllowed)
                .accessibilityLabel(isDownloaded ? "Remove download" : "Download")
            }
        }
        .contentShape(Rectangle())
        .contextMenu { TrackActions(track: track) }
        .accessibilityElement(children: .combine)
        .accessibilityAction(named: "Play", play)
    }
}

struct TrackActions: View {
    @EnvironmentObject private var catalog: CatalogStore
    let track: Track
    var body: some View {
        Button {
            Task { await catalog.toggleFavorite(track) }
        } label: { Label(catalog.isFavorite(track) ? "Remove Favorite" : "Add Favorite", systemImage: "heart") }
        Menu("Add to Playlist") {
            ForEach((catalog.library?.playlists ?? []).filter(\.isEditable)) { playlist in
                Button(playlist.name) { Task { await catalog.add(track, to: playlist) } }
            }
        }
    }
}

struct AccountToolbarButton: View {
    @EnvironmentObject private var auth: AuthStore
    @Binding var isPresented: Bool

    var body: some View {
        Button { isPresented = true } label: {
            switch auth.state {
            case let .signedIn(profile):
                AsyncImage(url: profile.avatarURL) { phase in
                    if case let .success(image) = phase {
                        image.resizable().scaledToFill()
                    } else {
                        Image(systemName: "person.crop.circle.fill")
                    }
                }
                .frame(width: 30, height: 30)
                .clipShape(Circle())
            default:
                Image(systemName: "person.crop.circle")
                    .font(.title2)
            }
        }
        .accessibilityLabel("Account")
    }
}
