from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.album.album import Album


@model
class Presaves(YandexMusicModel):
    """Класс, представляющий список предсохранённых альбомов.

    Attributes:
        upcoming_albums (:obj:`list` из :obj:`yandex_music.Album`, optional): Список предстоящих альбомов.
        released_albums (:obj:`list` из :obj:`yandex_music.Album`, optional): Список вышедших альбомов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    upcoming_albums: Optional[List['Album']] = None
    released_albums: Optional[List['Album']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.upcoming_albums, self.released_albums)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Presaves']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Presaves`: Список предсохранённых альбомов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Album

        cls_data['upcoming_albums'] = Album.de_list(cls_data.get('upcoming_albums'), client)
        cls_data['released_albums'] = Album.de_list(cls_data.get('released_albums'), client)

        return cls(client=client, **cls_data)
