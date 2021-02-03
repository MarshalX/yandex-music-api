from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Icon(YandexMusicObject):
    """Класс, представляющий иконку.

    Attributes:
        background_color (:obj:`str`): Цвет заднего фона в HEX.
        image_url (:obj:`str`): Ссылка на изображение.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        background_color (:obj:`str`): Цвет заднего фона в HEX.
        image_url (:obj:`str`): Ссылка на изображение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self, background_color: str, image_url: str, client: Optional['Client'] = None, **kwargs):
        self.background_color = background_color
        self.image_url = image_url

        self.client = client
        self._id_attrs = (self.background_color, self.image_url)

        super().handle_unknown_kwargs(self, **kwargs)

    def download(self, filename: str, size: str = '200x200') -> None:
        """Загрузка иконки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер иконки.
        """
        self.client.request.download(self.get_url(size), filename)

    def get_url(self, size: str = '200x200'):
        """Получение URL иконки.

        Args:
            size (:obj:`str`, optional): Размер иконки.
        """
        return f'https://{self.image_url.replace("%%", size)}'

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Icon']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Icon`: Иконка.
        """
        if not data:
            return None

        data = super(Icon, cls).de_json(data, client)

        return cls(client=client, **data)
