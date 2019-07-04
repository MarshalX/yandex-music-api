from yandex_music import YandexMusicObject


class Experiments(YandexMusicObject):
    """Класс представления каких-то свистелок-перделок, флажков, режимов экспериментальных функций.

    Attributes:
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.
        название_эксперимента (:obj:`str`, optional): Содержит режим или состояние, или функцию, или ещё что угодно.

    Args:
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Собственно тут и передаются все эти свистелки.
    """

    def __init__(self,
                 client=None,
                 **kwargs):
        self.__dict__.update(kwargs)

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Experiments`: Объект класса :class:`yandex_music.Experiments`.
        """
        if not data:
            return None

        data = super(Experiments, cls).de_json(data, client)

        return cls(client=client, **data)
