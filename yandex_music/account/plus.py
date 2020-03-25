from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Plus(YandexMusicObject):
    """Класс, представляющий `Plus` подписку.

    Attributes:
        has_plus (:obj:`bool`): Наличие.
        is_tutorial_completed (:obj:`bool`): Закончено ли руководство.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        has_plus (:obj:`bool`): Наличие.
        is_tutorial_completed (:obj:`bool`): Закончено ли руководство.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 has_plus: bool,
                 is_tutorial_completed: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.has_plus = has_plus
        self.is_tutorial_completed = is_tutorial_completed

        self.client = client
        self._id_attrs = (self.has_plus, self.is_tutorial_completed)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Plus']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Plus`: Plus подписка.
        """
        if not data:
            return None

        data = super(Plus, cls).de_json(data, client)

        return cls(client=client, **data)
