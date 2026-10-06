from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Cover


@model
class OpenGraphData(YandexMusicModel):
    """Класс, представляющий данные для Open Graph.

    Attributes:
        title (:obj:`str`): Заголовок.
        description (:obj:`str`): Описание.
        image (:obj:`yandex_music.Cover`): Изображение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    description: str
    image: 'Cover'
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.description, self.image)
