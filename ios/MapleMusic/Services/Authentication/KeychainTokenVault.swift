import Foundation
import Security

struct OAuthToken: Codable, Equatable, Sendable {
    let accessToken: String
    let tokenType: String
    let refreshToken: String?
    let expiresAt: Date?

    var isExpired: Bool {
        guard let expiresAt else { return false }
        return expiresAt <= Date().addingTimeInterval(30)
    }
}

struct BackendSession: Codable, Equatable, Sendable {
    let accessToken: String
    let expiresAt: Date
    let userID: String

    var isExpired: Bool {
        expiresAt <= Date().addingTimeInterval(30)
    }
}

private enum KeychainCodableStore {
    static func load<Value: Decodable>(service: String, account: String, as type: Value.Type) throws -> Value? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne,
        ]
        var item: CFTypeRef?
        let status = SecItemCopyMatching(query as CFDictionary, &item)
        if status == errSecItemNotFound { return nil }
        guard status == errSecSuccess, let data = item as? Data else {
            throw AuthError.keychain(status)
        }
        return try JSONDecoder().decode(type, from: data)
    }

    static func save<Value: Encodable>(_ value: Value, service: String, account: String) throws {
        let data = try JSONEncoder().encode(value)
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
        ]
        let attributes: [String: Any] = [
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
        ]
        let updateStatus = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)
        if updateStatus == errSecSuccess { return }
        guard updateStatus == errSecItemNotFound else {
            throw AuthError.keychain(updateStatus)
        }
        var insert = query
        attributes.forEach { insert[$0.key] = $0.value }
        let insertStatus = SecItemAdd(insert as CFDictionary, nil)
        guard insertStatus == errSecSuccess else { throw AuthError.keychain(insertStatus) }
    }

    static func clear(service: String, account: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
        ]
        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw AuthError.keychain(status)
        }
    }
}

actor KeychainTokenVault {
    private let service = "app.maplemusic.oauth"
    private let account: String

    init(account: String = "yandex-token") { self.account = account }

    func load() throws -> OAuthToken? {
        try KeychainCodableStore.load(service: service, account: account, as: OAuthToken.self)
    }

    func save(_ token: OAuthToken) throws {
        try KeychainCodableStore.save(token, service: service, account: account)
    }

    func clear() throws {
        try KeychainCodableStore.clear(service: service, account: account)
    }
}

actor BackendSessionVault {
    private let service = "app.maplemusic.backend-session"
    private let account = "current-session"

    func load() throws -> BackendSession? {
        try KeychainCodableStore.load(service: service, account: account, as: BackendSession.self)
    }

    func save(_ session: BackendSession) throws {
        try KeychainCodableStore.save(session, service: service, account: account)
    }

    func clear() throws {
        try KeychainCodableStore.clear(service: service, account: account)
    }
}
