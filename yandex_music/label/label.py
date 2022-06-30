from typing import Optional, Union, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model


@model
class LabelFull(YandexMusicObject):
    """Класс, представляющий лейбл

    Attributes:
        id (:obj:`int` | :obj:`str`): Уникальный идентификатор.
        name (:obj:`str`): Название.
        description (:obj:`str`, optional): описание.
        descriptionFormatted (:obj:`str`, optional): Описание лейбла. Только текст, без разметки.
        image (:obj:`str`, optional): ссылка на изобржение.
        links (:obj:`list` из :obj:`yandex_music.Link`, optional): Ссылки на ресурсы исполнителя.
        type (:obj:`str`, optional): тип лейбла.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
    """

    id: Union[str, int]
    name: Optional[str] = None
    description: Optional[str] = None
    description_formatted: Optional[str] = None
    image: Optional[str] = None
    links: Optional[List["Link"]] = None
    type: Optional[str] = None
    client: Optional["Client"] = None

    def get_artists(self):
        """Сокращение для::

        client.get_label_artists(label_id)
        """

        return self.client.get_label_artists(self.id)

    def get_albums(self):
        """Сокращение для::

        client.get_label_albums(label_id)
        """
        return self.client.get_label_albums(self.id)

    async def get_artists_async(self):
        """Сокращение для::

        client.get_label_artists(label_id)
        """

        return await self.client.get_label_artists(self.id)

    async def get_albums_async(self):
        """Сокращение для::

        client.get_label_albums(label_id)
        """
        return await self.client.get_label_albums(self.id)

    @classmethod
    def de_json(cls, data: dict, client: "Client") -> Optional["Label"]:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Label`: Label.
        """

        if not data:
            return None

        data = super(LabelFull, cls).de_json(data, client)
        from yandex_music import Link

        data["id"] = data.get("id")
        data["name"] = data.get("name")
        data["description"] = data.get("description")
        data["description_formatted"] = data.get("descriptionFormatted")
        data["image"] = data.get("image")
        data["links"] = Link.de_list(data.get("links"), client)
        data["type"] = data.get("type")

        return cls(client=client, **data)
