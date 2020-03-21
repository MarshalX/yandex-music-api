from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class MixLink(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 title: str,
                 url: str,
                 url_scheme: str,
                 text_color: str,
                 background_color: str,
                 background_image_uri: str,
                 cover_white: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.title = title
        self.url = url
        self.url_scheme = url_scheme
        self.text_color = text_color
        self.background_color = background_color
        self.background_image_uri = background_image_uri
        self.cover_white = cover_white

        self.client = client
        self._id_attrs = (self.url, self.title, self.url_scheme, self.text_color,
                          self.background_color, self.background_image_uri, self.cover_white)

    def download_background_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка заднего фона.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер заднего фона.
        """
        self.client.request.download(f'https://{self.background_image_uri.replace("%%", size)}', filename)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['MixLink']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MixLink`: TODO.
        """
        if not data:
            return None

        data = super(MixLink, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['MixLink']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.MixLink`: TODO.
        """
        if not data:
            return []

        mix_links = list()
        for mix_link in data:
            mix_links.append(cls.de_json(mix_link, client))

        return mix_links

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_background_image`
    downloadBackgroundImage = download_background_image
