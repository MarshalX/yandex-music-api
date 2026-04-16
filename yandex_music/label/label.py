from typing import TYPE_CHECKING, List, Optional, Union, cast

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Link


@model
class Label(YandexMusicModel):
    """Класс, представляющий лейбл.

    Note:
        Известные значения поля `type`: `musical`.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор лейбла.
        name (:obj:`str`): Название лейбла.
        description (:obj:`str`, optional): Описание.
        description_formatted (:obj:`str`, optional): Отформатированное описание.
        image (:obj:`str`, optional): Ссылка на изображение.
        links (:obj:`list` из :obj:`yandex_music.Link`, optional): Ссылки на ресурсы лейбла.
        type (:obj:`str`, optional): Тип лейбла.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    name: str
    description: Optional[str] = None
    description_formatted: Optional[str] = None
    image: Optional[str] = None
    links: Optional[List['Link']] = None
    type: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.name)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Label']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Label`: Лейбл.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Link

        cls_data['links'] = Link.de_list(cls_data.get('links'), client)

        return cls(client=client, **cls_data)

    @classmethod
    def de_list(cls, data: 'JSONType', client: 'ClientType') -> Union[List['Label'], List[str]]:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Note:
            Лейблы строками возвращаются, как минимум, в результатах поиска. В остальных местах это объекты.

        Returns:
            :obj:`list` из :obj:`yandex_music.Label` или :obj:`str`: Лейблы.
        """
        if isinstance(data, list) and all(isinstance(label, str) for label in data):
            return cast('List[str]', data)

        return super().de_list(data, client)
