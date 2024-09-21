from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Tag(YandexMusicModel):
    """Класс, представляющий тег (подборку).

    Attributes:
        id (:obj:`str`): Уникальный идентификатор тега.
        value (:obj:`str`): Значение тега (название в lower case).
        name (:obj:`str`): Название тега (отображаемое).
        og_description (:obj:`str`): Описание тега для OpenGraph.
        og_image (:obj:`str`, optional): Ссылка на изображение для OpenGraph.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    value: str
    name: str
    og_description: str
    og_image: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)

    # TODO (MarshalX) add download_og_image shortcut?
    #  https://github.com/MarshalX/yandex-music-api/issues/556
