from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Ratings(YandexMusicObject):
    """Класс, представляющий рейтинг исполнителя.

    Attributes:
        month (:obj:`int`): Значение ежемесячного рейтинга.
        week (:obj:`int`): Значение еженедельного рейтинга.
        day (:obj:`int`): Значение дневного рейтинга.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        month (:obj:`int`): Значение ежемесячного рейтинга.
        week (:obj:`int`, optional): Значение еженедельного рейтинга.
        day (:obj:`int`, optional): Значение дневного рейтинга.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 month: int,
                 week: Optional[int] = None,
                 day: Optional[int] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.week = week
        self.month = month

        self.day = day

        self.client = client
        self._id_attrs = (self.week, self.month)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Ratings']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Ratings`: Рейтинг исполнителя.
        """
        if not data:
            return None

        data = super(Ratings, cls).de_json(data, client)

        return cls(client=client, **data)
