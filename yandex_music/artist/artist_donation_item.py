from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist_donation_data import ArtistDonationData


@model
class ArtistDonationItem(YandexMusicModel):
    """Класс, представляющий элемент блока донатов артиста.

    Note:
        Известные значения поля ``type``: ``donation_item``.

    Attributes:
        type (:obj:`str`, optional): Тип элемента.
        data (:obj:`yandex_music.ArtistDonationData`, optional): Данные доната.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    data: Optional['ArtistDonationData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistDonationItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistDonationItem`: Элемент блока донатов артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.artist.artist_donation_data import ArtistDonationData

        cls_data['data'] = ArtistDonationData.de_json(cls_data.get('data'), client)

        return cls(client=client, **cls_data)
