from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist import Artist


@model
class Clip(YandexMusicModel):
    """Класс, представляющий видеоклип.

    Attributes:
        clip_id (:obj:`int`, optional): Уникальный идентификатор клипа.
        title (:obj:`str`, optional): Название клипа.
        version (:obj:`str`, optional): Версия клипа.
        player_id (:obj:`str`, optional): Идентификатор видеоплеера.
        uuid (:obj:`str`, optional): UUID клипа.
        thumbnail (:obj:`str`, optional): URL обложки клипа.
        preview_url (:obj:`str`, optional): URL превью видео.
        duration (:obj:`int`, optional): Длительность клипа в секундах.
        track_ids (:obj:`list` из :obj:`int`, optional): Список идентификаторов связанных треков.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список артистов клипа.
        disclaimers (:obj:`list` из :obj:`str`, optional): Список дисклеймеров.
        explicit (:obj:`bool`, optional): Содержит ли клип ненормативный контент.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    clip_id: Optional[int] = None
    title: Optional[str] = None
    version: Optional[str] = None
    player_id: Optional[str] = None
    uuid: Optional[str] = None
    thumbnail: Optional[str] = None
    preview_url: Optional[str] = None
    duration: Optional[int] = None
    track_ids: Optional[List[int]] = None
    artists: Optional[List['Artist']] = None
    disclaimers: Optional[List[str]] = None
    explicit: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.clip_id,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Clip']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Clip`: Видеоклип.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist

        cls_data['artists'] = Artist.de_list(cls_data.get('artists'), client)

        return cls(client=client, **cls_data)
