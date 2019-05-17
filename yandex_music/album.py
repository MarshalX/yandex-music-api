from datetime import datetime

from yandex_music import YandexMusicObject


class Album(YandexMusicObject):
    def __init__(self,
                 id,
                 title,
                 cover_uri,
                 track_count,
                 artists,
                 labels,
                 available,
                 available_for_premium_users,
                 content_warning=None,
                 original_release_year=None,
                 genre=None,
                 og_image=None,
                 buy=None,
                 recent=None,
                 very_important=None,
                 available_for_mobile=None,
                 available_partially=None,
                 bests=None,
                 year=None,
                 release_date=None,
                 type=None,
                 track_position=None,
                 regions=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.title = title
        self.cover_uri = cover_uri
        self.track_count = track_count
        self.artists = artists
        self.labels = labels
        self.available_for_premium_users = available_for_premium_users
        self.available = available

        self.genre = genre
        self.year = year
        self.release_date = datetime.fromisoformat(release_date) if release_date else release_date
        self.bests = bests
        self.og_image = og_image
        self.buy = buy
        self.recent = recent
        self.very_important = very_important
        self.available_for_mobile = available_for_mobile
        self.available_partially = available_partially
        self.type = type
        self.track_position = track_position
        self.regions = regions
        self.original_release_year = original_release_year
        self.content_warning = content_warning

        self.client = client
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Album, cls).de_json(data, client)
        from yandex_music import Artist, Label, TrackPosition
        data['artists'] = Artist.de_list(data.get('artists'), client)
        data['labels'] = Label.de_list(data.get('labels'), client)
        data['track_position'] = TrackPosition.de_json(data.get('track_position'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        albums = list()
        for album in data:
            albums.append(cls.de_json(album, client))

        return albums
