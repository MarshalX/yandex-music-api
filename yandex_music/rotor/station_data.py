from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class StationData(YandexMusicObject):
    """Класс, представляющий информацию о личной станции.

    Attributes:
        name (:obj:`str`): Название станции.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        name (:obj:`str`): Название станции.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self, name: str, client: Optional['Client'] = None, **kwargs) -> None:
        self.name = name

        self.client = client
        self._id_attrs = (self.name,)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['StationData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.StationData`: Информация о личной станции.
        """
        if not data:
            return None

        data = super(StationData, cls).de_json(data, client)

        return cls(client=client, **data)
