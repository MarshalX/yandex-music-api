from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class PlayCounter(YandexMusicObject):
    """Класс, представляющий счётчик дней.

    Note:
        Присутствует только у плейлиста дня. Счётчик считает количество дней подряд, на протяжении которых был
        прослушан плейлист.

    Attributes:
        value (:obj:`int`): Значение (количество дней).
        description (:obj:`str`): Описание счётчика.
        updated (:obj:`bool`): Обновлён ли сегодня (в этих сутках).
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        value (:obj:`int`): Значение (количество дней).
        description (:obj:`str`): Описание счётчика.
        updated (:obj:`bool`): Обновлён ли сегодня (в этих сутках).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 value: int,
                 description: str,
                 updated: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

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
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlayCounter`: Счетчик дней.
        """
        if not data:
            return None

        data = super(PlayCounter, cls).de_json(data, client)

        return cls(client=client, **data)
