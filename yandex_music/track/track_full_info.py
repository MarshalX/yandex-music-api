from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType, JSONType
    from yandex_music.track.track import Track


@model
class TrackFullInfo(YandexMusicModel):
    """Класс, представляющий полную информацию о треке.

    Attributes:
        track (:obj:`yandex_music.Track`, optional): Трек.
        similar_tracks (:obj:`list` из :obj:`yandex_music.Track`, optional): Список похожих треков.
        also_in_albums (:obj:`list` из :obj:`yandex_music.Track`, optional): Список треков из других альбомов.
        aliases (:obj:`list` из :obj:`str`, optional): Список псевдонимов трека.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список артистов с подробной информацией.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track: Optional['Track'] = None
    similar_tracks: Optional[List['Track']] = None
    also_in_albums: Optional[List['Track']] = None
    aliases: Optional[List[str]] = None
    artists: Optional[List['Artist']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackFullInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackFullInfo`: Полная информация о треке.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist, Track

        cls_data['track'] = Track.de_json(cls_data.get('track'), client)
        cls_data['similar_tracks'] = Track.de_list(cls_data.get('similar_tracks'), client)
        cls_data['also_in_albums'] = Track.de_list(cls_data.get('also_in_albums'), client)
        cls_data['artists'] = Artist.de_list(cls_data.get('artists'), client)

        return cls(client=client, **cls_data)
