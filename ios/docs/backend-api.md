# Custom API Gateway

Optional provider selected in Settings. This mode is separate from direct Yandex Music.
Enter an HTTPS base URL and the gateway's own token. The client validates it with `GET /v1/me`.
All requests carry `Authorization: Bearer <gateway-token>`; a Yandex credential is never
automatically copied into the gateway's credential store.

Responses are JSON matching the Codable models in `MapleMusic/Domain/MusicModels.swift`.
Dates use ISO 8601. Errors use HTTP status codes (401, 403, 404, 409, 429, 5xx).

| Request | Response |
| --- | --- |
| GET /v1/me | UserProfile |
| GET /v1/home | HomeFeed |
| GET /v1/search?q=… | [Track] |
| GET /v1/library | MusicLibrary |
| GET /v1/playlists/{id} | Playlist |
| POST /v1/playlists, body `{ "name": "…" }` | Playlist |
| PUT /v1/playlists/{id}/tracks/{trackID} | 204 |
| DELETE /v1/playlists/{id}/tracks/{trackID} | 204 |
| PUT /v1/library/favorites/{trackID} | 204 |
| DELETE /v1/library/favorites/{trackID} | 204 |
| GET /v1/tracks/{id}/playback?quality=automatic\|high\|lossless | PlaybackAsset |
| GET /v1/tracks/{id}/lyrics | Lyrics or 404 |

The backend returns media accessible to the current account and explicit download permission.
Playback URLs must be HTTPS, playable without the API Authorization header (e.g. signed URLs).
`codec`, `bitDepth`, and `sampleRate` describe the returned media, not merely the request.
For `encraw`, `decryptionKey` is a hex AES key and `transport` is `encraw`; the counter starts at zero.
HLS can be streamed via AVPlayer, but offline HLS packages are not implemented.

Minimal playback response:

```json
{
  "url": "https://media.example.com/signed-track.flac",
  "quality": "lossless",
  "codec": "flac",
  "bitDepth": 16,
  "sampleRate": 44100,
  "allowsOfflineDownload": true
}
```

Lyrics lines require UUID `id`, seconds `time`, and UTF-8 `text`.
