from typing import TYPE_CHECKING, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Value(YandexMusicModel):
    """Класс, представляющий значение(переменную).

    Note:
        Для шкал (:class:`yandex_music.DiscreteScale`) значение числовое.

    Attributes:
        value (:obj:`str` | :obj:`int`): Значение.
        name (:obj:`str`): Название.
        image_url (:obj:`str`, optional): Ссылка на изображение значения.
        serialized_seed (:obj:`str`, optional): Значение в виде сида для радио (например, `settingDiversity:favorite`).
        unspecified (:obj:`bool`, optional): Является ли значение значением по умолчанию («Любое»).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    value: Union[str, int]
    name: str
    image_url: Optional[str] = None
    serialized_seed: Optional[str] = None
    unspecified: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.value, self.name)
