from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Context(YandexMusicObject):
    """Класс, представляющий содержимое очереди.

    Note:
        Известные значения поля `type`: `various`, `my_music`, `radio`, `playlist`, `artist`.

        Тип `various` используется при прослушивании из раздела "Моя музыка" с сайта, а `my_music` с мобильных клиентов.

        Поле `description` зачастую есть только когда `type` имеет значение `my_music` или `various`.

        При `type` равным `my_music` или `various` поле `id` отсутствует.

    Attributes:
        type (:obj:`str`): Тип содержимого (по чём построена очередь).
        id (:obj:`str`): Уникальный идентификатор типа содержимого (плейлиста, альбома и т.д.).
        description (:obj:`str`): Описание содержимого (например, название плейлиста, радиостанции).
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type_ (:obj:`str`): Тип содержимого (по чём построена очередь).
        id_ (:obj:`str`, optional): Уникальный идентификатор типа содержимого (плейлиста, альбома и т.д.).
        description (:obj:`str`, optional): Описание содержимого (например, название плейлиста, радиостанции).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    def __init__(
        self,
        type_: str,
        id_: Optional[str] = None,
        description: Optional[str] = None,
        client: Optional['Client'] = None,
        **kwargs,
    ):
        self.type = type_

        self.id = id_
        self.description = description

        self.client = client
        self._id_attrs = (
            self.type,
            self.id,
        )

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Context']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Context`: Содержимое очереди.
        """
        if not data:
            return None

        data = super(Context, cls).de_json(data, client)

        return cls(client=client, **data)
