from typing import TYPE_CHECKING, List, Optional

from yandex_music import JSONType, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import AlbumEvent, ArtistEvent, ClientType, Track


@model
class Event(YandexMusicModel):
    """Класс, представляющий событие фида.

    Note:
        Известные значения поля `type`: `tracks`, `artists`, `albums`, `notification`.

        Поле `message` заполнено только когда `type` равен `notification`.

        Примером значения поля `type_for_from` может служить `recommended-similar-artists`.

        Наличие данных в `tracks`, `albums`, `artists` напрямую зависит от `type`.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор события.
        type (:obj:`str`): Тип события.
        type_for_from (:obj:`str`, optional): Откуда пришло событие.
        title (:obj:`str`, optional): Заголовок.
        tracks (:obj:`list` из :obj:`yandex_music.Track`, optional): Список треков.
        artists (:obj:`list` из :obj:`yandex_music.ArtistEvent`, optional): Список артистов с похожими и популярными
            треками.
        albums (:obj:`list` из :obj:`yandex_music.AlbumEvent`, optional): Список альбомов с треками.
        message (:obj:`str`, optional): Сообщение уведомления.
        device (:obj:`str`, optional): Устройство, с которого пришло уведомление.
        tracks_count (:obj:`int`, optional): Количество треков (возможно, уже не используется).
        genre (:obj:`str`, optional): Жанр треков.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    type: str
    type_for_from: Optional[str] = None
    title: Optional[str] = None
    tracks: List['Track'] = []
    artists: List['ArtistEvent'] = []
    albums: List['AlbumEvent'] = []
    message: Optional[str] = None
    device: Optional[str] = None
    tracks_count: Optional[int] = None
    genre: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.type)

    @classmethod
    def de_json(cls, data: JSONType, client: 'ClientType') -> Optional['Event']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Event`: Событие фида.
        """
        if not cls.is_dict_model_data(data):
            return None

        data = cls.cleanup_data(data, client)
        from yandex_music import AlbumEvent, ArtistEvent, Track

        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['albums'] = AlbumEvent.de_list(data.get('albums'), client)
        data['artists'] = ArtistEvent.de_list(data.get('artists'), client)

        return cls(client=client, **data)
