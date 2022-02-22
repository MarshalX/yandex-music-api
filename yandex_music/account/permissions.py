from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Permissions(YandexMusicObject):
    """Класс, представляющий информацию о правах пользователя, их изначальных значениях и даты окончания.

    Attributes:
        until (:obj:`str`): Дата окончания прав.
        values (:obj:`list` из :obj:`str`): Список прав.
        default (:obj:`list` из :obj:`str`): Список изначальных прав.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    until: str
    values: List[str]
    default: List[str]
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.until, self.values, self.default)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Permissions']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Permissions`: Информация о правах пользователя, их изначальных значениях и даты
                окончания.
        """
        if not data:
            return None

        data = super(Permissions, cls).de_json(data, client)

        return cls(client=client, **data)
