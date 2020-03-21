from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Description(YandexMusicObject):
    """Класс, представляющий описание исполнителя из другого источника.

    Note:
        Очень редкий объект, у минимального количества исполнителей.
        Обычно берётся информация из википедии.

    Attributes:
        text (:obj:`str`): Описание исполнителя.
        url (:obj:`str`): Ссылка на источник.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        text (:obj:`str`): Описание исполнителя.
        url (:obj:`str`): Ссылка на источник.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 text: str,
                 url: Optional[str] = None, # возможно, вообще параметр должен всегда называться uri
                 uri: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.text = text
        self.url = url if url else uri if uri else ''

        self.client = client
        self._id_attrs = (self.text, self.url)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Description']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Description`: Объект класса :class:`yandex_music.Descriptions`.
        """
        if not data:
            return None

        data = super(Description, cls).de_json(data, client)

        return cls(client=client, **data)
