from datetime import datetime

from yandex_music import YandexMusicObject


class Album(YandexMusicObject):
    def __init__(self,
                 id,
                 title,
                 type,
                 year,
                 release_date,
                 cover_uri,
                 og_image,
                 genre,
                 buy,
                 track_count,
                 recent,
                 very_important,
                 artists,
                 labels,
                 available,
                 available_for_premium_users,
                 available_for_mobile,
                 available_partially,
                 bests,
                 track_position=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.title = title
        self.type = type
        self.year = year
        self.release_date = datetime.fromisoformat(release_date)
        self.cover_uri = cover_uri
        self.og_image = og_image
        self.genre = genre
        self.buy = buy
        self.track_count = track_count
        self.recent = recent
        self.very_important = very_important
        self.artists = artists
        self.labels = labels
        self.bests = bests
        self.available_partially = available_partially
        self.available_for_mobile = available_for_mobile
        self.available_for_premium_users = available_for_premium_users
        self.available = available

        self.track_position = track_position

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
