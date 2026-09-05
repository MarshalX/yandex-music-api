# Verification — 2026-09-05

## Executed locally (Windows)

- Parsed all current Swift source/test files with tree-sitter; no syntax errors after fixes.
- Parsed XcodeGen, xtool and GitHub Actions YAML, resource plists, asset JSON and PCM WAV metadata.
- Downloaded XcodeGen 2.46.0 and verified SHA256:
  `4d9e34b62172d645eed6457cac13fc222569974098ef4ee9c3368bedf0196806`.
- Confirmed the upstream `actions/checkout@v7` and `actions/upload-artifact@v7` tags exist.
- Guest `GET https://api.music.yandex.net/account/status`: HTTP 200, JSON.
- Guest `GET https://api.music.yandex.net/search?text=Maple&type=track&page=0`: HTTP 451.
  This is not evidence that authenticated catalogue/playback works from this network.

## Not executed

No Swift/iOS SDK or macOS runtime is available locally. No GitHub remote with write/Actions access
was supplied. Consequently Swift type checking, XCTest, actual device login, audio decoding,
download/relaunch UI checks and the final IPA build have **not run**.
No IPA is claimed as produced by this version.

XCTest includes mixed-type API IDs and Cyrillic metadata, LRC offset/multiple tags,
an AES-CTR known-answer vector, account isolation and offline metadata persistence,
download permission checks, PKCE and demo-service checks. These are checked in, not reported as passed.

## Protocol references

The adapter is a Swift implementation of the HTTP data formats, not an embedded Python runtime.

- [MarshalX/yandex-music-api](https://github.com/MarshalX/yandex-music-api), inspected commit
  `0fa54f2d32084a9e461bce41890d1c9ab70d91aa`: account/search/tracks/playlists/likes/lyrics/device auth.
- [File info discussion](https://github.com/MarshalX/yandex-music-api/issues/656): lossless response format.
- [llistochek/yandex-music-downloader](https://github.com/llistochek/yandex-music-downloader), inspected commit
  `9d33d6aaefae3cb882d02822e59cf0796c33a651`: encraw transport parameters, response key and AES-CTR counter.
- [GitHub macOS runner image](https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md):
  Xcode 16.4 and iOS 18.5 simulator availability.

Public protocol signing constants and device-client parameters can change upstream.
They are not credentials for a user's account. Personal access tokens are obtained at runtime
and stored only in the device Keychain. Lossless/download requests still require server authorization.
