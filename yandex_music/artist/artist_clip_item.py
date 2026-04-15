from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist_clip_data import ArtistClipData


@model
class ArtistClipItem(YandexMusicModel):
    """Класс, представляющий элемент блока клипов артиста.

    Note:
        Известные значения поля ``type``: ``clip``.

    Attributes:
        type (:obj:`str`, optional): Тип элемента.
        data (:obj:`yandex_music.ArtistClipData`, optional): Данные клипа.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    data: Optional['ArtistClipData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistClipItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistClipItem`: Элемент блока клипов артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.artist.artist_clip_data import ArtistClipData

        cls_data['data'] = ArtistClipData.de_json(cls_data.get('data'), client)

        return cls(client=client, **cls_data)
