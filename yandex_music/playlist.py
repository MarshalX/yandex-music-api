from datetime import datetime

from yandex_music import YandexMusicObject


class Playlist(YandexMusicObject):
    def __init__(self,
                 owner,
                 uid,
                 kind,
                 title,
                 revision,
                 snapshot,
                 track_count,
                 visibility,
                 collective,
                 created,
                 modified,
                 available,
                 is_banner,
                 is_premiere,
                 duration_ms,
                 cover,
                 og_image,
                 tags,
                 prerolls,
                 made_for,
                 play_counter,
                 likes_count=None,
                 generated_playlist_type=None,
                 animated_cover_uri=None,
                 ever_played=None,
                 description=None,
                 description_formatted=None,
                 is_for_from=None,
                 client=None,
                 **kwargs):
        self.owner = owner
        self.uid = uid
        self.kind = kind
        self.title = title
        self.revision = revision
        self.snapshot = snapshot
        self.track_count = track_count
        self.visibility = visibility
        self.collective = collective
        self.created = datetime.fromisoformat(created)
        self.modified = datetime.fromisoformat(modified)
        self.available = available
        self.is_banner = is_banner
        self.is_premiere = is_premiere
        self.duration_ms = duration_ms
        self.cover = cover
        self.og_image = og_image
        self.tags = tags
        self.prerolls = prerolls
        self.made_for = made_for
        self.play_counter = play_counter

        self.likes_count = likes_count
        self.animated_cover_uri = animated_cover_uri
        self.description = description
        self.description_formatted = description_formatted
        self.ever_played = ever_played
        self.generated_playlist_type = generated_playlist_type
        self.is_for_from = is_for_from

        self.client = client
        self._id_attrs = (self.uid,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Playlist, cls).de_json(data, client)
        from yandex_music import User, MadeFor, Cover, PlayCounter
        data['owner'] = User.de_json(data.get('owner'), client)
        data['cover'] = Cover.de_json(data.get('cover'), client)
        data['made_for'] = MadeFor.de_json(data.get('made_for'), client)
        data['play_counter'] = PlayCounter.de_json(data.get('play_counter'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        playlists = list()
        for playlist in data:
            playlists.append(cls.de_json(playlist, client))

        return playlists
