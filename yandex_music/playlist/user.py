from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class User(YandexMusicObject):
    """Класс, представляющий пользователя.

    Attributes:
        uid (:obj:`int`): Идентификатор пользователя.
        login (:obj:`str`): Логин пользователя.
        name (:obj:`str`): Имя пользователя.
        sex (:obj:`str`): Пол пользователя.
        verified (:obj:`bool`): Участвует ли пользователь в генерации плейлистов дня и т.д., и т.п.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        uid (:obj:`int`): Идентификатор пользователя.
        login (:obj:`str`): Логин пользователя.
        name (:obj:`str`): Имя пользователя.
        sex (:obj:`str`): Пол пользователя.
        verified (:obj:`bool`): Участвует ли пользователь в генерации плейлистов дня и т.д., и т.п.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 uid: int,
                 login: str,
                 name: str,
                 sex: str,
                 verified: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.uid = uid
        self.login = login
        self.name = name
        self.sex = sex
        self.verified = verified

        self.client = client
        self._id_attrs = (self.uid, self.login)

    def download_avatar(self, filename: str, format_: str = 'normal') -> None:
        """Загрузка изображения пользователя.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            format_ (:obj:`str`, optional): Формат желаемого изображения (`normal`, `orig`, `small`, `big`).
        """
        self.client.request.download(f'https://upics.yandex.net/{self.uid}/{format_}', filename)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['User']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.User`: Пользователь.
        """
        if not data:
            return None

        data = super(User, cls).de_json(data, client)

        return cls(client=client, **data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_avatar`
    downloadAvatar = download_avatar
