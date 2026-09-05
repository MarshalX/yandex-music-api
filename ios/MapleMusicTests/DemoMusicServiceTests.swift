import XCTest
@testable import MapleMusic

final class DemoMusicServiceTests: XCTestCase {
    func testDemoServiceSupportsCoreFlows() async throws {
        let service = DemoMusicService()
        let home = try await service.home()
        XCTAssertFalse(home.featured.isEmpty)

        let results = try await service.search(query: "Northern")
        XCTAssertEqual(results.first?.id, "northern-lights")

        let library = try await service.library()
        XCTAssertFalse(library.playlists.isEmpty)

        let lyrics = try await service.lyrics(for: home.featured[0])
        XCTAssertFalse(lyrics?.lines.isEmpty ?? true)
    }
}

