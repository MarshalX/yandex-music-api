from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist import Artist
    from yandex_music.clip.clip import Clip


@model
class ArtistClipData(YandexMusicModel):
    """Класс, представляющий данные клипа артиста.

    Attributes:
        clip (:obj:`yandex_music.Clip`, optional): Клип.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список артистов клипа.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    clip: Optional['Clip'] = None
    artists: Optional[List['Artist']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.clip,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistClipData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistClipData`: Данные клипа артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist
        from yandex_music.clip.clip import Clip

        cls_data['clip'] = Clip.de_json(cls_data.get('clip'), client)
        cls_data['artists'] = Artist.de_list(cls_data.get('artists'), client)

        return cls(client=client, **cls_data)
