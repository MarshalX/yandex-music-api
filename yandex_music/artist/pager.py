from yandex_music import YandexMusicObject


class Pager(YandexMusicObject):
    """Класс представляющий пагинатор.

    Attributes:
        total (:obj:`int`): Всего треков.
        page (:obj:`int`): Номер страницы.
        per_page (:obj:`int`): Количество треков на странице.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        total (:obj:`int`): Всего треков.
        page (:obj:`int`): Номер страницы.
        per_page (:obj:`int`): Количество треков на странице.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 total,
                 page,
                 per_page,
                 client=None,
                 **kwargs):
        self.total = total
        self.page = page
        self.per_page = per_page

        self.client = client
        self._id_attrs = (self.total, self.page, self.per_page)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Pager`: Объект класса :class:`yandex_music.Pager`.
        """
        if not data:
            return None

        data = super(Pager, cls).de_json(data, client)

        return cls(client=client, **data)
