from typing import TYPE_CHECKING, Optional, List, Dict

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Title, Icon, Images


class Genre(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: str,
                 weight: int,
                 composer_top: bool,
                 title: str,
                 titles: Dict[str, Optional['Title']],
                 images: Optional['Images'],
                 show_in_menu: bool,
                 full_title: Optional[str] = None,
                 url_part: Optional[str] = None,
                 color: Optional[str] = None,
                 radio_icon: Optional['Icon'] = None,
                 sub_genres: List['Genre'] = None,
                 hide_in_regions=None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.weight = weight
        self.composer_top = composer_top
        self.title = title
        self.titles = titles
        self.images = images
        self.show_in_menu = show_in_menu

        self.full_title = full_title
        self.url_part = url_part
        self.color = color
        self.radio_icon = radio_icon
        self.sub_genres = sub_genres
        self.hide_in_regions = hide_in_regions

        self.client = client
        self._id_attrs = (self.id, self.weight, self.composer_top, self.title, self.images, self.show_in_menu)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Genre']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Genre`: Объект класса :class:`yandex_music.Genre`.
        """
        if not data:
            return None

        data = super(Genre, cls).de_json(data, client)
        from yandex_music import Title, Icon, Images
        data['titles'] = Title.de_dict(data.get('titles'), client)
        data['images'] = Images.de_json(data.get('images'), client)
        data['radio_icon'] = Icon.de_json(data.get('radio_icon'), client)
        data['sub_genres'] = Genre.de_list(data.get('sub_genres'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Genre']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Genre`: Список объектов класса :class:`yandex_music.Genre`.
        """
        if not data:
            return []

        genres = list()
        for genre in data:
            genres.append(cls.de_json(genre, client))

        return genres
