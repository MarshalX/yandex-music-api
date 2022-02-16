from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Pager(YandexMusicObject):
    """Класс, представляющий пагинатор.

    Attributes:
        total (:obj:`int`): Всего треков.
        page (:obj:`int`): Номер страницы.
        per_page (:obj:`int`): Количество треков на странице.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    total: int
    page: int
    per_page: int
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.total, self.page, self.per_page)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Pager']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Pager`: Пагинатор.
        """
        if not data:
            return None

        data = super(Pager, cls).de_json(data, client)

        return cls(client=client, **data)
