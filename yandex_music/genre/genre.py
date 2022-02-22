from typing import TYPE_CHECKING, Optional, List, Dict

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Title, Icon, Images


@model
class Genre(YandexMusicObject):
    """Класс, представляющий жанр музыки.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор жанра.
        weight (:obj:`int`): Вес TODO (возможно, чем выше показатель, тем больше нравится пользователю).
        composer_top (:obj:`bool`): TODO.
        title (:obj:`str`): Заголовок жанра.
        titles (:obj:`dict`): Словарь заголовков на разных языках, где ключ - язык.
        images (:obj:`yandex_music.Images`): Изображение жанра.
        show_in_menu (:obj:`bool`): Показывать в меню.
        show_in_regions (:obj:`list` из :obj:`int`, optional): Список регионов в которых отображается жанр в списках.
        full_title (:obj:`str`, optional): Полный заголовок.
        url_part (:obj:`str`, optional): Часть ссылки на жанр для открытия в браузере.
        color (:obj:`str`, optional): Цвет фона изображения.
        radio_icon (:obj:`yandex_music.Icon`, optional): Иконка радио жанра.
        sub_genres (:obj:`list` из :obj:`yandex_music.Genre`, optional): Поджанры текущего жанра музыки.
        hide_in_regions (:obj:`list`, optional): В каких регионах скрывать жанр.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    weight: int
    composer_top: bool
    title: str
    titles: Dict[str, Optional['Title']]
    images: Optional['Images']
    show_in_menu: bool
    show_in_regions: Optional[list] = None
    full_title: Optional[str] = None
    url_part: Optional[str] = None
    color: Optional[str] = None
    radio_icon: Optional['Icon'] = None
    sub_genres: List['Genre'] = None
    hide_in_regions = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.weight, self.composer_top, self.title, self.images, self.show_in_menu)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Genre']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Genre`: Жанр музыки.
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
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Genre`: Жанры музыки.
        """
        if not data:
            return []

        return [cls.de_json(genre, client) for genre in data]
