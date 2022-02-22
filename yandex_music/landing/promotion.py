from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Promotion(YandexMusicObject):
    """Класс, представляющий продвижение (рекламу).

    Note:
        В цвете может как оказаться HEX (`#6c65a9`), так и какой-нибудь `transparent`.

        Ссылка со схемой отличается от просто ссылки наличием `yandexmusic://` в начале.

    Attributes:
        promo_id (:obj:`str`): Уникальный идентификатор рекламы.
        title (:obj:`str`): Заголовок.
        subtitle (:obj:`str`): Подзаголовок.
        heading (:obj:`str`): Верхний заголовок.
        url (:obj:`str`): Ссылка.
        url_scheme (:obj:`str`): Ссылка с схемой.
        text_color (:obj:`str`): Цвет текста.
        gradient (:obj:`str`): Градиент TODO.
        image (:obj:`str`): Ссылка на рекламное изображение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    promo_id: str
    title: str
    subtitle: str
    heading: str
    url: str
    url_scheme: str
    text_color: str
    gradient: str
    image: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (
            self.promo_id,
            self.title,
            self.subtitle,
            self.heading,
            self.url,
            self.url_scheme,
            self.text_color,
            self.gradient,
            self.image,
        )

    def download_image(self, filename: str, size: str = '300x300') -> None:
        """Загрузка рекламного изображения.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер изображения.
        """
        self.client.request.download(f'https://{self.image.replace("%%", size)}', filename)

    async def download_image_async(self, filename: str, size: str = '300x300') -> None:
        """Загрузка рекламного изображения.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер изображения.
        """
        await self.client.request.download(f'https://{self.image.replace("%%", size)}', filename)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Promotion']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Promotion`: Продвижение (реклама).
        """
        if not data:
            return None

        data = super(Promotion, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Promotion']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Promotion`: Продвижения (реклама).
        """
        if not data:
            return []

        promotions = list()
        for promotion in data:
            promotions.append(cls.de_json(promotion, client))

        return promotions

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_image`
    downloadImage = download_image
    #: Псевдоним для :attr:`download_image_async`
    downloadImageAsync = download_image_async
