from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class AdParams(YandexMusicObject):
    def __init__(self,
                 partner_id: Union[str, int],
                 category_id: Union[str, int],
                 page_ref: str,
                 target_ref: str,
                 other_params: str,
                 ad_volume: int,
                 genre_id=None,
                 genre_name=None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.partner_id = partner_id
        self.category_id = category_id
        self.page_ref = page_ref
        self.target_ref = target_ref
        self.other_params = other_params
        self.ad_volume = ad_volume

        self.genre_id = genre_id
        self.genre_name = genre_name

        self.client = client
        self._id_attrs = (self.partner_id, self.category_id, self.page_ref,
                          self.target_ref, self.other_params, self.ad_volume)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['AdParams']:
        if not data:
            return None

        data = super(AdParams, cls).de_json(data, client)

        return cls(client=client, **data)
