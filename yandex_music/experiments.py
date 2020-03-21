from typing import TYPE_CHECKING, Optional


from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Experiments(YandexMusicObject):
    """Класс, представляющий какие-то свистелки-перделки, флажки, режимы экспериментальных функций.

    Attributes:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        название_эксперимента (:obj:`str`, optional): Содержит режим или состояние, или функцию, или ещё что угодно.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Собственно тут и передаются все эти свистелки.
    """

    def __init__(self,
                 client: Optional['Client'] = None,
                 **kwargs):
        self.__dict__.update(kwargs)

        self.client = client

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Experiments']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Experiments`: Какие-то свистелки-перделки, флажки, режимы экспериментальных функций.
        """
        if not data:
            return None

        data = super(Experiments, cls).de_json(data, client)

        return cls(client=client, **data)
