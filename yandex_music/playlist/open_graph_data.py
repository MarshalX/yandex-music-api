from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Cover


class OpenGraphData(YandexMusicObject):
    """Класс, представляющий данные для Open Graph.

    Attributes:
        title (:obj:`str`): Заголовок.
        description (:obj:`str`): Описание.
        image (:obj:`yandex_music.Cover`): Изображение.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        title (:obj:`str`): Заголовок.
        description (:obj:`str`): Описание.
        image (:obj:`yandex_music.Cover`): Изображение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self, title: str, description: str, image: 'Cover', client: Optional['Client'] = None, **kwargs
    ) -> None:
        self.title = title
        self.description = description
        self.image = image

        self.client = client
        self._id_attrs = (self.title, self.description, self.image)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['OpenGraphData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.OpenGraphData`: Данные для Open Graph.
        """
        if not data:
            return None

        data = super(OpenGraphData, cls).de_json(data, client)
        from yandex_music import Cover

        data['image'] = Cover.de_json(data.get('image'), client)

        return cls(client=client, **data)
