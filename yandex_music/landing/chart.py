from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, TrackId


class Chart(YandexMusicObject):
    """Класс, представляющий элемент чарта.

    Note:
        Смещение - это количество позиций, на которые трек поднялся или опустился в чарте.

    Attributes:
        position (:obj:`int`): Позиция.
        progress (:obj:`str`): TODO.
        listeners (:obj:`int`): Количество слушателей.
        shift (:obj:`int`): Смещение.
        bg_color (:obj:`str`): Цвет заднего фона.
        track_id (:obj:`yandex_music.TrackId` | :obj:`None`): Уникальный идентификатор трека.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        position (:obj:`int`): Позиция.
        progress (:obj:`str`): TODO.
        listeners (:obj:`int`): Количество слушателей.
        shift (:obj:`int`): Смещение.
        bg_color (:obj:`str`, optional): Цвет заднего фона.
        track_id (:obj:`yandex_music.TrackId`, optional): Уникальный идентификатор трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 position: int,
                 progress: str,
                 listeners: int,
                 shift: int,
                 bg_color: Optional[str] = None,
                 track_id: Optional['TrackId'] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.position = position
        self.progress = progress
        self.listeners = listeners
        self.shift = shift

        self.bg_color = bg_color
        self.track_id = track_id

        self.client = client
        self._id_attrs = (self.position, self.progress, self.listeners, self.shift, self.track_id)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Chart']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Chart`: Элемент чарта.
        """
        if not data:
            return None

        data = super(Chart, cls).de_json(data, client)
        from yandex_music import TrackId
        data['track_id'] = TrackId.de_json(data.get('track_id'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Chart']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Chart`: Чарт.
        """
        if not data:
            return []

        return [cls.de_json(chart, client) for chart in data]
