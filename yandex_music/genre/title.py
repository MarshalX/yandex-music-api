from typing import TYPE_CHECKING, Dict, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


@model
class Title(YandexMusicModel):
    """Класс, представляющий заголовок жанра.

    Attributes:
        title (:obj:`str`): Заголовок.
        full_title (:obj:`str`, optional): Полный заголовок.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    full_title: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.full_title)

    @classmethod
    def de_dict(cls, data: 'JSONType', client: 'ClientType') -> Dict[str, 'Title']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`dict`): Словарь с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`dict` где ключ это язык :obj:`str`, а значение :obj:`yandex_music.Title`: Заголовки жанров.
        """
        if not cls.is_dict_model_data(data):
            return {}

        titles: Dict[str, 'Title'] = {}
        for lang, raw_title in data.items():
            title = cls.de_json(raw_title, client)
            if title:
                titles.update({lang: title})

        return titles
