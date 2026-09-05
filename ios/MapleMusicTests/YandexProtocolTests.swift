import Foundation
import XCTest
@testable import MapleMusic

final class YandexProtocolTests: XCTestCase {
    func testMixedIdentifiersAndCyrillicMetadata() throws {
        let json = #"{"id":123,"title":"Тестовая песня","durationMs":123456,"available":true,"availableForPremiumUsers":true,"artists":[{"id":"7","name":"Артист"}],"albums":[{"id":42,"title":"Альбом"}],"coverUri":"avatars.yandex.net/get-music-content/%%"}"#
        let track = try JSONDecoder().decode(YandexJSON.self, from: Data(json.utf8)).track()
        XCTAssertEqual(track?.id, "123:42")
        XCTAssertEqual(track?.title, "Тестовая песня")
        XCTAssertEqual(track?.artist.name, "Артист")
        XCTAssertEqual(track?.duration, 123.456)
        XCTAssertEqual(track?.artwork.url?.scheme, "https")
        XCTAssertTrue(track?.downloadAllowed == true)
    }

    func testUnavailableTrackCannotBeDownloaded() throws {
        let json = #"{"id":"1","title":"Unavailable","available":false}"#
        let track = try JSONDecoder().decode(YandexJSON.self, from: Data(json.utf8)).track()
        XCTAssertFalse(track?.downloadAllowed ?? true)
    }

    func testLRCMultipleTagsOffsetsAndStableOrdering() {
        let source = "[offset:-250]\n[00:03.50]Позже\n[00:01.00][00:02.00]Припев\n[ar:Автор]"
        let lines = LRCParser.parse(source)
        XCTAssertEqual(lines.map(\.time), [0.75, 1.75, 3.25])
        XCTAssertEqual(lines.map(\.text), ["Припев", "Припев", "Позже"])
    }

    func testEncrawAESCTRZeroCounterVector() throws {
        let root = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: root, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: root) }
        let source = root.appendingPathComponent("encrypted")
        let output = root.appendingPathComponent("plain")
        // AES-128(0, 0) = 66e94bd4ef8a2c3b884cfa59ca342b2e.
        let ciphertext: [UInt8] = [0x66, 0xe9, 0x4b, 0xd4, 0xef, 0x8a, 0x2c, 0x3b, 0x88, 0x4c, 0xfa, 0x59, 0xca, 0x34, 0x2b, 0x2e,
            0x58, 0xe2, 0xfc, 0xce, 0xfa, 0x7e, 0x30, 0x61, 0x36, 0x7f, 0x1d, 0x57, 0xa4, 0xe7, 0x45, 0x5a]
        try Data(ciphertext).write(to: source)
        try MediaFileLoader.decrypt(source: source, destination: output, hexKey: String(repeating: "0", count: 32))
        XCTAssertEqual(try Data(contentsOf: output), Data(repeating: 0, count: 32))
    }

    func testProviderRejectsUnsafeAddressesAndSeparatesCredentials() throws {
        var config = ProviderConfiguration()
        config.endpoint = "http://example.com"
        XCTAssertThrowsError(try config.validatedURL())
        config.endpoint = "https://user:password@example.com"
        XCTAssertThrowsError(try config.validatedURL())
        let original = ProviderConfiguration().credentialID
        config.endpoint = "https://another.example.com"
        XCTAssertNotEqual(config.credentialID, original)
    }
}
