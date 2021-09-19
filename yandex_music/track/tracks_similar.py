from typing import TYPE_CHECKING, Optional, List, Iterator

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Track


@model
class SimilarTracks(YandexMusicObject):
    """Класс, представляющий список похожих треков на другой трек.

    Attributes:
        track (:obj:`yandex_music.Track`): Трек.
        similar_tracks (:obj:`list` из :obj:`yandex_music.Track`): Похожие треки на `track`.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track: Optional['Track']
    similar_tracks: List['Track']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.track, self.similar_tracks)

    def __getitem__(self, item) -> 'Track':
        return self.similar_tracks[item]

    def __iter__(self) -> Iterator['Track']:
        return iter(self.similar_tracks)

    def __len__(self) -> int:
        return len(self.similar_tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['SimilarTracks']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SimilarTracks`: Список похожих треков на другой трек.
        """
        if not data:
            return None

        data = super(SimilarTracks, cls).de_json(data, client)
        from yandex_music import Track

        data['track'] = Track.de_json(data.get('track'), client)
        data['similar_tracks'] = Track.de_list(data.get('similar_tracks'), client)

        return cls(client=client, **data)
