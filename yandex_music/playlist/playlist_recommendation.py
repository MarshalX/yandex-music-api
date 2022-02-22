from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Track


@model
class PlaylistRecommendations(YandexMusicObject):
    """Класс, представляющий рекомендации для плейлиста.

    Attributes:
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Список рекомендованных треков.
        batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tracks: List['Track']
    batch_id: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.batch_id, self.tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlaylistRecommendations']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlaylistRecommendations`: Рекомендации для плейлиста.
        """
        if not data:
            return None

        data = super(PlaylistRecommendations, cls).de_json(data, client)
        from yandex_music import Track

        data['tracks'] = Track.de_list(data.get('tracks'), client)

        return cls(client=client, **data)
