import Foundation
import XCTest
@testable import MapleMusic

final class OfflineStoreTests: XCTestCase {
    func testCopiesAndRemovesLicensedLocalAsset() async throws {
        let root = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString, isDirectory: true)
        defer { try? FileManager.default.removeItem(at: root) }
        try FileManager.default.createDirectory(at: root, withIntermediateDirectories: true)
        let source = root.appendingPathComponent("source.wav")
        try Data([0x52, 0x49, 0x46, 0x46]).write(to: source)

        let store = OfflineStore(root: root.appendingPathComponent("offline", isDirectory: true))
        let artist = Artist(id: "artist", name: "Artist")
        let track = Track(id: "track/with unsafe path", title: "Track", artist: artist, albumTitle: "Album", duration: 10)
        let asset = PlaybackAsset(
            url: source,
            quality: .lossless,
            codec: "PCM",
            bitDepth: 16,
            sampleRate: 44_100,
            expiresAt: nil,
            allowsOfflineDownload: true
        )

        let entry = try await store.save(track: track, asset: asset)
        XCTAssertFalse(entry.relativePath.contains("/"))
        let containsAfterSave = await store.contains(trackID: track.id)
        let localAsset = await store.localAsset(for: track)
        XCTAssertTrue(containsAfterSave)
        XCTAssertNotNil(localAsset)

        let reopened = OfflineStore(root: root.appendingPathComponent("offline", isDirectory: true))
        let restored = await reopened.entries()
        XCTAssertEqual(restored.first?.track, track)

        await store.setScope("another-account")
        let otherAccountAsset = await store.localAsset(for: track)
        XCTAssertNil(otherAccountAsset)

        try await reopened.remove(trackID: track.id)
        let containsAfterRemoval = await reopened.contains(trackID: track.id)
        XCTAssertFalse(containsAfterRemoval)
    }

    func testRejectsAssetWithoutDownloadPermission() async {
        let root = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString, isDirectory: true)
        defer { try? FileManager.default.removeItem(at: root) }
        let store = OfflineStore(root: root)
        let track = Track(
            id: "locked",
            title: "Locked",
            artist: Artist(id: "artist", name: "Artist"),
            albumTitle: "Album",
            duration: 10,
            downloadAllowed: false
        )
        let asset = PlaybackAsset(
            url: root.appendingPathComponent("missing.wav"),
            quality: .high,
            codec: "AAC",
            bitDepth: nil,
            sampleRate: nil,
            expiresAt: nil,
            allowsOfflineDownload: false
        )
        do {
            try await store.save(track: track, asset: asset)
            XCTFail("Expected offline permission failure")
        } catch let error as MusicServiceError {
            XCTAssertEqual(error, .offlineUnavailable)
        } catch {
            XCTFail("Unexpected error: \(error)")
        }
    }
}
