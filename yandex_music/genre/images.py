from yandex_music import YandexMusicObject


class Images(YandexMusicObject):
    def __init__(self,
                 _208x208=None,
                 _300x300=None,
                 client=None,
                 **kwargs):
        self._208x208 = _208x208
        self._300x300 = _300x300

        self.client = client

    def download_208x208(self, filename):
        """Загрузка изображения 208x208.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """

        self.client.request.download(self._208x208, filename)

    def download_300x300(self, filename):
        """Загрузка изображения 300x300.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """

        self.client.request.download(self._300x300, filename)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Images, cls).de_json(data, client)

        return cls(client=client, **data)

