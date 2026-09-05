import XCTest
@testable import MapleMusic

final class LyricsSynchronizerTests: XCTestCase {
    private let lines = [
        LyricsLine(time: 2, text: "One"),
        LyricsLine(time: 5, text: "Two"),
        LyricsLine(time: 9, text: "Three"),
    ]

    func testBeforeFirstLineReturnsNil() {
        XCTAssertNil(LyricsSynchronizer.activeLineIndex(at: 1.99, lines: lines))
    }

    func testBoundarySelectsMatchingLine() {
        XCTAssertEqual(LyricsSynchronizer.activeLineIndex(at: 5, lines: lines), 1)
    }

    func testAfterLastLineKeepsLastLine() {
        XCTAssertEqual(LyricsSynchronizer.activeLineIndex(at: 100, lines: lines), 2)
    }

    func testEmptyLyricsReturnsNil() {
        XCTAssertNil(LyricsSynchronizer.activeLineIndex(at: 1, lines: []))
    }
}

