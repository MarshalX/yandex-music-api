from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Tag(YandexMusicObject):
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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Tag']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Tag`: Тег.
        """
        if not data:
            return None

        data = super(Tag, cls).de_json(data, client)

        return cls(client=client, **data)

    # TODO (MarshalX) add download_og_image shortcut?
