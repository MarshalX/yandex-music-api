from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Description(YandexMusicObject):
    """Класс, представляющий описание исполнителя из другого источника.

    Note:
        Очень редкий объект, у минимального количества исполнителей.
        Обычно берётся информация из википедии.

    Attributes:
        text (:obj:`str`): Описание исполнителя.
        uri (:obj:`str`): Ссылка на источник.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    text: str
    uri: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.text, self.uri)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Description']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Description`: Описание исполнителя из другого источника.
        """
        if not data:
            return None

        data = super(Description, cls).de_json(data, client)

        return cls(client=client, **data)
