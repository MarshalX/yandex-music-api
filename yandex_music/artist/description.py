from yandex_music import YandexMusicObject


class Description(YandexMusicObject):
    def __init__(self,
                 text,
                 url,
                 client=None,
                 **kwargs):
        self.text = text
        self.url = url

        self.client = client
        self._id_attrs = (self.text, self.url)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Description`: Объект класса :class:`yandex_music.Descriptions`.
        """

        if not data:
            return None

        data = super(Description, cls).de_json(data, client)

        return cls(client=client, **data)
