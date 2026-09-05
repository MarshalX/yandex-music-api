import CryptoKit
import Foundation

struct OfflineEntry: Codable, Hashable, Identifiable, Sendable {
    var id: String { trackID }
    let trackID: String
    let relativePath: String
    let quality: AudioQuality
    let codec: String
    let bitDepth: Int?
    let sampleRate: Int?
    let byteCount: Int64
    let savedAt: Date
    var track: Track? = nil
    var lyrics: Lyrics? = nil
}

actor OfflineStore {
    private struct Manifest: Codable {
        var entries: [String: OfflineEntry] = [:]
    }

    private let baseRoot: URL
    private var root: URL
    private var manifestURL: URL
    private var manifest: Manifest

    init(root: URL? = nil) {
        let resolvedRoot: URL
        if let root {
            resolvedRoot = root
        } else {
            let support = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask).first!
            resolvedRoot = support.appendingPathComponent("Offline", isDirectory: true)
        }
        self.root = resolvedRoot
        self.baseRoot = resolvedRoot
        manifestURL = resolvedRoot.appendingPathComponent("manifest.json")
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        manifest = (try? Data(contentsOf: manifestURL)).flatMap { try? decoder.decode(Manifest.self, from: $0) } ?? Manifest()
    }

    func setScope(_ scope: String) {
        root = baseRoot.appendingPathComponent(safeFileName(scope), isDirectory: true)
        manifestURL = root.appendingPathComponent("manifest.json")
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        manifest = (try? Data(contentsOf: manifestURL)).flatMap { try? decoder.decode(Manifest.self, from: $0) } ?? Manifest()
    }

    func localLyrics(for trackID: String) -> Lyrics? { manifest.entries[trackID]?.lyrics }

    func entries() -> [OfflineEntry] {
        manifest.entries.values.filter { contains(trackID: $0.trackID) }.sorted { $0.savedAt > $1.savedAt }
    }

    func contains(trackID: String) -> Bool {
        guard let entry = manifest.entries[trackID] else { return false }
        let url = root.appendingPathComponent(entry.relativePath)
        return isInsideRoot(url) && FileManager.default.fileExists(atPath: url.path)
    }

    func localAsset(for track: Track) -> PlaybackAsset? {
        guard let entry = manifest.entries[track.id] else { return nil }
        let url = root.appendingPathComponent(entry.relativePath)
        guard isInsideRoot(url), FileManager.default.fileExists(atPath: url.path) else { return nil }
        return PlaybackAsset(
            url: url,
            quality: entry.quality,
            codec: entry.codec,
            bitDepth: entry.bitDepth,
            sampleRate: entry.sampleRate,
            expiresAt: nil,
            allowsOfflineDownload: true
        )
    }

    @discardableResult
    func save(track: Track, asset: PlaybackAsset, lyrics: Lyrics? = nil) async throws -> OfflineEntry {
        guard track.downloadAllowed, asset.allowsOfflineDownload else {
            throw MusicServiceError.offlineUnavailable
        }
        try ensureRoot()
        let activeRoot = root
        let ext = MediaFileLoader.fileExtension(for: asset)
        let relativePath = "\(safeFileName(track.id))-\(UUID().uuidString).\(ext)"
        let destination = root.appendingPathComponent(relativePath)
        guard isInsideRoot(destination) else { throw MusicServiceError.offlineUnavailable }

        let temporary = root.appendingPathComponent(".\(UUID().uuidString).download")
        defer { try? FileManager.default.removeItem(at: temporary) }
        try await MediaFileLoader.download(asset, to: temporary)
        guard root == activeRoot else { throw CancellationError() }
        try FileManager.default.moveItem(at: temporary, to: destination)
        var resourceValues = URLResourceValues()
        resourceValues.isExcludedFromBackup = true
        var mutableDestination = destination
        try? mutableDestination.setResourceValues(resourceValues)
        let attributes = try FileManager.default.attributesOfItem(atPath: destination.path)
        let byteCount = (attributes[.size] as? NSNumber)?.int64Value ?? 0
        let entry = OfflineEntry(
            trackID: track.id,
            relativePath: relativePath,
            quality: asset.quality,
            codec: asset.codec,
            bitDepth: asset.bitDepth,
            sampleRate: asset.sampleRate,
            byteCount: byteCount,
            savedAt: Date(), track: track, lyrics: lyrics
        )
        let previous = manifest.entries[track.id]
        manifest.entries[track.id] = entry
        do { try persistManifest() }
        catch {
            manifest.entries[track.id] = previous
            try? FileManager.default.removeItem(at: destination)
            throw error
        }
        if let previous {
            let old = root.appendingPathComponent(previous.relativePath)
            if isInsideRoot(old) { try? FileManager.default.removeItem(at: old) }
        }
        return entry
    }

    func remove(trackID: String) throws {
        guard let entry = manifest.entries.removeValue(forKey: trackID) else { return }
        let target = root.appendingPathComponent(entry.relativePath)
        guard isInsideRoot(target) else { throw MusicServiceError.offlineUnavailable }
        if FileManager.default.fileExists(atPath: target.path) {
            try FileManager.default.removeItem(at: target)
        }
        try persistManifest()
    }

    private func ensureRoot() throws {
        try FileManager.default.createDirectory(at: root, withIntermediateDirectories: true)
        var resourceValues = URLResourceValues()
        resourceValues.isExcludedFromBackup = true
        var mutableRoot = root
        try? mutableRoot.setResourceValues(resourceValues)
    }

    private func persistManifest() throws {
        try ensureRoot()
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        try encoder.encode(manifest).write(to: manifestURL, options: .atomic)
    }

    private func isInsideRoot(_ url: URL) -> Bool {
        let rootPath = root.standardizedFileURL.pathComponents
        let targetPath = url.standardizedFileURL.pathComponents
        return targetPath.starts(with: rootPath)
    }

    private func safeFileName(_ value: String) -> String {
        let digest = SHA256.hash(data: Data(value.utf8))
        return digest.map { String(format: "%02x", $0) }.joined()
    }
}
