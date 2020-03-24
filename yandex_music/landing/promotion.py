from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


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
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
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
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 promo_id: str,
                 title: str,
                 subtitle: str,
                 heading: str,
                 url: str,
                 url_scheme: str,
                 text_color: str,
                 gradient: str,
                 image: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.promo_id = promo_id
        self.title = title
        self.subtitle = subtitle
        self.heading = heading
        self.url = url
        self.url_scheme = url_scheme
        self.text_color = text_color
        self.gradient = gradient
        self.image = image

        self.client = client
        self._id_attrs = (self.promo_id, self.title, self.subtitle, self.heading,
                          self.url, self.url_scheme, self.text_color, self.gradient, self.image)

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
