from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist_skeleton_block_data import ArtistSkeletonBlockData


@model
class ArtistSkeletonBlock(YandexMusicModel):
    """Класс, представляющий блок скелетона артиста.

    Note:
        Известные значения поля ``type``: ``TABS``, ``ARTIST_RELEASE``, ``ARTIST_POPULAR_TRACKS``,
        ``FAMILIAR_YOU``, ``ARTIST_ALBUMS``, ``ARTIST_PLAYLISTS``, ``BANDLINK_SCANNER``,
        ``ARTIST_COMPILATIONS``, ``SIMILAR_ARTISTS``.

    Attributes:
        id (:obj:`str`, optional): Идентификатор блока.
        type (:obj:`str`, optional): Тип блока.
        data (:obj:`yandex_music.ArtistSkeletonBlockData`, optional): Данные блока.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[str] = None
    type: Optional[str] = None
    data: Optional['ArtistSkeletonBlockData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.type)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistSkeletonBlock']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistSkeletonBlock`: Блок скелетона артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.artist.artist_skeleton_block_data import ArtistSkeletonBlockData

        cls_data['data'] = ArtistSkeletonBlockData.de_json(cls_data.get('data'), client)

        return cls(client=client, **cls_data)
