from typing import TYPE_CHECKING, Iterator, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Track


@model
class SimilarTracks(YandexMusicModel):
    """Класс, представляющий список похожих треков на другой трек.

    Attributes:
        track (:obj:`yandex_music.Track`): Трек.
        similar_tracks (:obj:`list` из :obj:`yandex_music.Track`): Похожие треки на `track`.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track: Optional['Track']
    similar_tracks: List['Track']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track, self.similar_tracks)

    def __getitem__(self, item: int) -> 'Track':
        return self.similar_tracks[item]

    def __iter__(self) -> Iterator['Track']:
        return iter(self.similar_tracks)

    def __len__(self) -> int:
        return len(self.similar_tracks)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['SimilarTracks']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SimilarTracks`: Список похожих треков на другой трек.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Track

        cls_data['track'] = Track.de_json(data.get('track'), client)
        cls_data['similar_tracks'] = Track.de_list(data.get('similar_tracks'), client)

        return cls(client=client, **cls_data)  # type: ignore
