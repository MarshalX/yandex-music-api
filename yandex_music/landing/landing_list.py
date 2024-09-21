from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import JSONType, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, PlaylistId


@model
class LandingList(YandexMusicModel):
    """Класс, представляющий список объектов лендинга.

    Note:
        Известные значения поля `type`: `new-playlists`, `new-releases`, `podcasts`.

        В зависимости от типа будет заполнено то, или иное поле.

    Attributes:
        type (:obj:`str`): Тип результата.
        type_for_from (:obj:`str`): Откуда пришло событие.
        title (:obj:`str`): Заголовок страницы.
        id (:obj:`str`, optional): Уникальный идентификатор списка.
        new_releases (:obj:`list` из :obj:`int`, optional): Новые альбомы.
        new_playlists (:obj:`list` из :obj:`PlaylistId`, optional): Новые плейлисты.
        podcasts (:obj:`list` из :obj:`int`, optional): Подкасты.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    type_for_from: str
    title: str
    id: Optional[str] = None
    new_releases: List[int] = field(default_factory=list)
    new_playlists: List['PlaylistId'] = field(default_factory=list)
    podcasts: List[int] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.new_releases, self.new_playlists, self.podcasts)

    @classmethod
    def de_json(cls, data: JSONType, client: 'ClientType') -> Optional['LandingList']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LandingList`: Список объектов лендинга.
        """
        if not cls.is_dict_model_data(data):
            return None

        data = cls.cleanup_data(data, client)
        from yandex_music import PlaylistId

        data['new_playlists'] = PlaylistId.de_list(data.get('new_playlists'), client)

        return cls(client=client, **data)
