from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Context(YandexMusicModel):
    """Класс, представляющий содержимое очереди.

    Note:
        Известные значения поля `type`: `various`, `my_music`, `radio`, `playlist`, `artist`.

        Тип `various` используется при прослушивании из раздела "Моя музыка" с сайта, а `my_music` с мобильных клиентов.

        Поле `description` зачастую есть только когда `type` имеет значение `my_music` или `various`.

        При `type` равным `my_music` или `various` поле `id` отсутствует.

    Attributes:
        type (:obj:`str`): Тип содержимого (по чём построена очередь).
        id (:obj:`str`, optional): Уникальный идентификатор типа содержимого (плейлиста, альбома и т.д.).
        description (:obj:`str`, optional): Описание содержимого (например, название плейлиста, радиостанции).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    id: Optional[str] = None
    description: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.id)
