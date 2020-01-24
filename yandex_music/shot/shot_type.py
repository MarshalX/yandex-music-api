from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class ShotType(YandexMusicObject):
    """Класс, представляющий тип шота от Алисы.

    Attributes:
        id_ (:obj:`str`): Уникальный идентификатор типа.
        title (:obj:`str`): Заголовок шота.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        id_ (:obj:`str`): Уникальный идентификатор типа.
        title (:obj:`str`): Заголовок шота.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: str,
                 title: str,
                 client: Optional['Client'] = None,
                 **kwargs):
        self.id_ = id_
        self.title = title

        self.client = client
        self._id_attrs = (self.id_, self.title)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ShotType']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.ShotType`: Объект класса :class:`yandex_music.ShotType`.
        """
        if not data:
            return None

        data = super(ShotType, cls).de_json(data, client)

        return cls(client=client, **data)
