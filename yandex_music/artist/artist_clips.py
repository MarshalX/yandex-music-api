from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist_clip_item import ArtistClipItem
    from yandex_music.pager import Pager


@model
class ArtistClips(YandexMusicModel):
    """Класс, представляющий блок клипов артиста.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.ArtistClipItem`, optional): Список элементов клипов.
        pager (:obj:`yandex_music.Pager`, optional): Пагинация.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: Optional[List['ArtistClipItem']] = None
    pager: Optional['Pager'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.items, self.pager)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistClips']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistClips`: Блок клипов артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Pager
        from yandex_music.artist.artist_clip_item import ArtistClipItem

        cls_data['items'] = ArtistClipItem.de_list(cls_data.get('items'), client)
        cls_data['pager'] = Pager.de_json(cls_data.get('pager'), client)

        return cls(client=client, **cls_data)
