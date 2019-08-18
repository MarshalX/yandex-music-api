from yandex_music import YandexMusicObject


class User(YandexMusicObject):
    def __init__(self,
                 uid,
                 login,
                 name,
                 sex,
                 verified,
                 client=None,
                 **kwargs):
        self.uid = uid
        self.login = login
        self.name = name
        self.sex = sex
        self.verified = verified

        self.client = client
        self._id_attrs = (self.uid,)

    def download_avatar(self, filename, format='normal'):
        """Загрузка изображения пользователя.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            format (:obj:`str`): Формат желаемого изображения (normal, orig, small, big).
        """

        self.client.request.download(f'https://upics.yandex.net/{self.uid}/{format}', filename)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(User, cls).de_json(data, client)

        return cls(client=client, **data)

    # camelCase псевдонимы

    """Псевдоним для :attr:`download_avatar`"""
    downloadAvatar = download_avatar
