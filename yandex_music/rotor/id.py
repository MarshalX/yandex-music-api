from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Id(YandexMusicObject):
    """Класс, представляющий уникальный идентификатор станции.

    Note:
        Известные типы станций: `user`, `genre`.

    Attributes:
        type (:obj:`str`): Тип станции.
        tag (:obj:`str`): Тег станции.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type_ (:obj:`str`): Тип станции.
        tag (:obj:`str`): Тег станции.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: str,
                 tag: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.type = type_
        self.tag = tag

        self.client = client
        self._id_attrs = (self.type, self.tag)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Id']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Id`: Уникальный идентификатор станции.
        """
        if not data:
            return None

        data = super(Id, cls).de_json(data, client)

        return cls(client=client, **data)
