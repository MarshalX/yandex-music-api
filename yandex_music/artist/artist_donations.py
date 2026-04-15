from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist_donation_item import ArtistDonationItem


@model
class ArtistDonations(YandexMusicModel):
    """Класс, представляющий блок донатов артиста.

    Attributes:
        donations (:obj:`list` из :obj:`yandex_music.ArtistDonationItem`, optional): Список донатов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    donations: Optional[List['ArtistDonationItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.donations,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistDonations']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistDonations`: Блок донатов артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.artist.artist_donation_item import ArtistDonationItem

        cls_data['donations'] = ArtistDonationItem.de_list(cls_data.get('donations'), client)

        return cls(client=client, **cls_data)
