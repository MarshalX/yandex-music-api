from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class PlayCounter(YandexMusicObject):
    def __init__(self,
                 value: int,
                 description: str,
                 updated: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.value = value
        self.description = description
        self.updated = updated

        self.client = client
        self._id_attrs = (self.value, self.description, self.updated)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlayCounter']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.PlayCounter`: Объект класса :class:`yandex_music.PlayCounter`.
        """
        if not data:
            return None

        data = super(PlayCounter, cls).de_json(data, client)

        return cls(client=client, **data)
