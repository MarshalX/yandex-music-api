from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Artist, Track


@model
class ArtistEvent(YandexMusicObject):
    """Класс, представляющий артиста в событии фида.

    Attributes:
        artist (:obj:`yandex_music.Artist` | :obj:`None`): Артист.
        tracks (:obj:`list` :obj:`yandex_music.Track`): Треки.
        similar_to_artists_from_history (:obj:`list` :obj:`yandex_music.Artist`): Похожие артисты из истории.
        subscribed (:obj:`bool`): Подписан ли на событие.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist']
    tracks: List['Track']
    similar_to_artists_from_history: List['Artist']
    subscribed: Optional['bool'] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.artist, self.tracks, self.similar_to_artists_from_history)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ArtistEvent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistEvent`: Артист из события фида.
        """
        if not data:
            return None

        data = super(ArtistEvent, cls).de_json(data, client)
        from yandex_music import Artist, Track

        data['artist'] = Artist.de_json(data.get('artist'), client)
        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['similar_to_artists_from_history'] = Artist.de_list(data.get('similar_to_artists_from_history'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['ArtistEvent']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.ArtistEvent`: Артисты из события фида.
        """
        if not data:
            return []

        artist_events = list()
        for artist_event in data:
            artist_events.append(cls.de_json(artist_event, client))

        return artist_events
