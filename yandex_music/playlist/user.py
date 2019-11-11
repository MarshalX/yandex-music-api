from yandex_music import YandexMusicObject


class User(YandexMusicObject):
    """Класс представляющий пользователя.

    Attributes:
        uid (:obj:`int`): Идентификатор пользователя.
        login (:obj:`str`): Логин пользователя.
        name (:obj:`str`): Имя пользователя.
        sex (:obj:`str`): Пол пользователя.
        verified (:obj:`bool`): Участвует ли пользователь в генерации плейлистов дня и т.д., и т.п.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex Music.

    Args:
        uid (:obj:`int`): Идентификатор пользователя.
        login (:obj:`str`): Логин пользователя.
        name (:obj:`str`): Имя пользователя.
        sex (:obj:`str`): Пол пользователя.
        verified (:obj:`bool`): Участвует ли пользователь в генерации плейлистов дня и т.д., и т.п.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

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
        self._id_attrs = (self.uid, self.login)

    def download_avatar(self, filename, format='normal'):
        """Загрузка изображения пользователя.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            format (:obj:`str`, optional): Формат желаемого изображения (normal, orig, small, big).
        """

        self.client.request.download(f'https://upics.yandex.net/{self.uid}/{format}', filename)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.User`: Объект класса :class:`yandex_music.User`.
        """
        if not data:
            return None

        data = super(User, cls).de_json(data, client)

        return cls(client=client, **data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_avatar`
    downloadAvatar = download_avatar
