from yandex_music import YandexMusicObject


class Plus(YandexMusicObject):
    """Класс представляющий Plus подписку.

    Attributes:
        has_plus (:obj:`bool`): Наличие.
        is_tutorial_completed (:obj:`bool`): Закончено ли руководство.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        has_plus (:obj:`bool`): Наличие.
        is_tutorial_completed (:obj:`bool`): Закончено ли руководство.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 has_plus,
                 is_tutorial_completed,
                 client=None,
                 **kwargs):
        self.has_plus = has_plus
        self.is_tutorial_completed = is_tutorial_completed

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Plus`: Объект класса :class:`yandex_music.Plus`.
        """
        if not data:
            return None

        data = super(Plus, cls).de_json(data, client)

        return cls(client=client, **data)
