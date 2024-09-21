from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Cover, JSONType


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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['OpenGraphData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.OpenGraphData`: Данные для Open Graph.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Cover

        cls_data['image'] = Cover.de_json(data.get('image'), client)

        return cls(client=client, **cls_data)  # type: ignore
