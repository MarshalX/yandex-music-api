from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Permissions(YandexMusicModel):
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

    def __post_init__(self) -> None:
        self._id_attrs = (self.until, self.values, self.default)
