from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, ContentRestrictions, Cover, JSONType


@model
class PinData(YandexMusicModel):
    """Класс, представляющий данные закреплённого элемента.

    Note:
        Для артистов используется поле `name`, для альбомов и плейлистов — `title`.

        Поле `playlist_uuid` доступно только для плейлистов.

        Поле `content_restrictions` может содержать информацию о доступности и ограничениях.

    Attributes:
        id (:obj:`int`, optional): Уникальный идентификатор (для артистов и альбомов).
        uid (:obj:`int`, optional): Уникальный идентификатор пользователя (для плейлистов).
        kind (:obj:`int`, optional): Номер плейлиста.
        playlist_uuid (:obj:`str`, optional): UUID плейлиста.
        name (:obj:`str`, optional): Имя артиста.
        title (:obj:`str`, optional): Название альбома или плейлиста.
        cover (:obj:`yandex_music.Cover`, optional): Обложка.
        content_restrictions (:obj:`yandex_music.ContentRestrictions`, optional): Ограничения контента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[int] = None
    uid: Optional[int] = None
    kind: Optional[int] = None
    playlist_uuid: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    cover: Optional['Cover'] = None
    content_restrictions: Optional['ContentRestrictions'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.uid, self.kind, self.name, self.title)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['PinData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PinData`: Данные закреплённого элемента.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import ContentRestrictions, Cover

        cls_data['cover'] = Cover.de_json(cls_data.get('cover'), client)
        cls_data['content_restrictions'] = ContentRestrictions.de_json(cls_data.get('content_restrictions'), client)

        return cls(client=client, **cls_data)
