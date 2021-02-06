from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Tag(YandexMusicObject):
    """Класс, представляющий тег (подборку).

    Attributes:
        id (:obj:`str`): Уникальный идентификатор тега.
        value (:obj:`str`): Значение тега (название в lower case).
        name (:obj:`str`): Название тега (отображаемое).
        og_description (:obj:`str`): Описание тега для OpenGraph.
        og_image (:obj:`str`): Ссылка на изображение для OpenGraph.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id (:obj:`str`): Уникальный идентификатор тега.
        value (:obj:`str`): Значение тега (название в lower case).
        name (:obj:`str`): Название тега (отображаемое).
        og_description (:obj:`str`): Описание тега для OpenGraph.
        og_image (:obj:`str`, optional): Ссылка на изображение для OpenGraph.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self,
        id_: str,
        value: str,
        name: str,
        og_description: str,
        og_image: Optional[str] = None,
        client: Optional['Client'] = None,
        **kwargs,
    ) -> None:
        self.id = id_
        self.value = value
        self.name = name
        self.og_description = og_description

        self.og_image = og_image

        self.client = client
        self._id_attrs = (self.id,)

        super().handle_unknown_kwargs(self, **kwargs)

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
