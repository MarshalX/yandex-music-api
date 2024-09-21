from typing import TYPE_CHECKING, List, Optional, Union, cast

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


@model
class Label(YandexMusicModel):
    """Класс, представляющий лейбл альбома.

    Attributes:
        id (:obj:`int`): Идентификатор альбома.
        name (:obj:`str`): Название альбома.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    name: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.name)

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
            return cast(List[str], data)

        return super().de_list(data, client)  # type: ignore
