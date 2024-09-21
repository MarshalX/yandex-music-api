from typing import TYPE_CHECKING, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class AdParams(YandexMusicModel):
    """Класс, представляющий параметры рекламного объявления.

    Note:
        Известные дополнительные параметры(`other_params`): `user:{ID}`.

    Attributes:
        partner_id (:obj:`str` | :obj:`int`): Уникальный идентификатор заказчика рекламы.
        category_id (:obj:`str` | :obj:`int`): Уникальный идентификатор категории рекламы.
        page_ref (:obj:`str`): Ссылка на ссылающуюся страницу.
        target_ref (:obj:`str`): Ссылка на целевую страницу.
        other_params (:obj:`str`): Другие параметры.
        ad_volume (:obj:`int`): Громкость воспроизводимой рекламы.
        genre_id (:obj:`str`, optional): Уникальный идентификатор жанра.
        genre_name (:obj:`str`, optional): Название жанра.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    partner_id: Union[str, int]
    category_id: Union[str, int]
    page_ref: str
    target_ref: str
    other_params: str
    ad_volume: int
    genre_id: Optional[str] = None
    genre_name: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (
            self.partner_id,
            self.category_id,
            self.page_ref,
            self.target_ref,
            self.other_params,
            self.ad_volume,
        )
