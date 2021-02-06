from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Brand(YandexMusicObject):
    """Класс, представляющий бренд плейлиста.

    Note:
        Отслеживание просмотров на сторонник сервисах бренда, рекомендация следующего контента.

    Attributes:
        image (:obj:`str`): Ссылка на изображение.
        background (:obj:`str`): Цвет заднего фона.
        reference (:obj:`str`): URI ссылка на содержимое.
        pixels (:obj:`list` из :obj:`str`): Ссылки на gif изображения для отслеживания просмотров (web beacon).
        theme (:obj:`str`): Тема оформления.
        playlist_theme (:obj:`str`): Тема плейлиста TODO.
        button (:obj:`str`): Текст кнопки.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        image (:obj:`str`): Ссылка на изображение.
        background (:obj:`str`): Цвет заднего фона.
        reference (:obj:`str`): URI ссылка на содержимое.
        pixels (:obj:`list` из :obj:`str`): Ссылки на gif изображения для отслеживания просмотров (web beacon).
        theme (:obj:`str`): Тема оформления.
        playlist_theme (:obj:`str`): Тема плейлиста TODO.
        button (:obj:`str`): Текст кнопки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self,
        image: str,
        background: str,
        reference: str,
        pixels: List[str],
        theme: str,
        playlist_theme: str,
        button: str,
        client: Optional['Client'] = None,
        **kwargs,
    ) -> None:
        self.image = image
        self.background = background
        self.reference = reference
        self.pixels = pixels
        self.theme = theme
        self.playlist_theme = playlist_theme
        self.button = button

        self.client = client
        self._id_attrs = (self.image, self.reference, self.pixels)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Brand']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Brand`: Бренд плейлиста.
        """
        if not data:
            return None

        data = super(Brand, cls).de_json(data, client)

        return cls(client=client, **data)
