import CryptoKit
import Foundation
import Security

struct PKCEPair: Equatable, Sendable {
    let verifier: String
    let challenge: String
}

enum PKCE {
    static func make(byteCount: Int = 48) throws -> PKCEPair {
        var bytes = [UInt8](repeating: 0, count: byteCount)
        let status = SecRandomCopyBytes(kSecRandomDefault, bytes.count, &bytes)
        guard status == errSecSuccess else {
            throw AuthError.randomGenerationFailed(status)
        }
        let verifier = Data(bytes).base64URLEncodedString()
        return PKCEPair(verifier: verifier, challenge: challenge(for: verifier))
    }

    static func state() throws -> String {
        try make(byteCount: 32).verifier
    }

    static func challenge(for verifier: String) -> String {
        let digest = SHA256.hash(data: Data(verifier.utf8))
        return Data(digest).base64URLEncodedString()
    }
}

private extension Data {
    func base64URLEncodedString() -> String {
        base64EncodedString()
            .replacingOccurrences(of: "+", with: "-")
            .replacingOccurrences(of: "/", with: "_")
            .replacingOccurrences(of: "=", with: "")
    }
}
