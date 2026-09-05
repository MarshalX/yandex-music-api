import XCTest
@testable import MapleMusic

final class PKCETests: XCTestCase {
    func testRFC7636ChallengeVector() {
        let verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
        XCTAssertEqual(PKCE.challenge(for: verifier), "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM")
    }

    func testGeneratedVerifierHasValidLengthAndAlphabet() throws {
        let pair = try PKCE.make()
        XCTAssertGreaterThanOrEqual(pair.verifier.count, 43)
        XCTAssertLessThanOrEqual(pair.verifier.count, 128)
        XCTAssertNil(pair.verifier.range(of: "[^A-Za-z0-9._~-]", options: .regularExpression))
        XCTAssertEqual(pair.challenge, PKCE.challenge(for: pair.verifier))
    }
}

