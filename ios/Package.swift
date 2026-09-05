// swift-tools-version: 6.0

import PackageDescription

let package = Package(
    name: "MapleMusic",
    platforms: [.iOS(.v17)],
    products: [
        .library(name: "MapleMusic", targets: ["MapleMusic"]),
    ],
    targets: [
        .target(
            name: "MapleMusic",
            path: "MapleMusic",
            exclude: [
                "Resources/Info.plist",
                "Resources/XTool-Info.plist",
                "Resources/Assets.xcassets",
                "Resources/PrivacyInfo.xcprivacy",
            ],
            resources: [
                .copy("Resources/DemoAudio"),
            ]
        ),
        .testTarget(
            name: "MapleMusicTests",
            dependencies: ["MapleMusic"],
            path: "MapleMusicTests"
        ),
    ],
    swiftLanguageModes: [.v5]
)
