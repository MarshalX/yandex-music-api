from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class MetatagSortByValue(YandexMusicModel):
    """Класс, представляющий доступное значение сортировки списка метатега.

    Note:
        Известные значения поля `value`: `popular`, `new`.

    Attributes:
        value (:obj:`str`, optional): Идентификатор значения сортировки.
        title (:obj:`str`, optional): Отображаемое название сортировки.
        active (:obj:`bool`, optional): Применена ли эта сортировка в текущем ответе.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    value: Optional[str] = None
    title: Optional[str] = None
    active: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.value, self.active)
