from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Id, Sequence

from yandex_music import YandexMusicObject


class StationTracksResult(YandexMusicObject):
    def __init__(self,
                 id_: Optional['Id'],
                 sequence: List['Sequence'],
                 batch_id: str,
                 pumpkin: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.sequence = sequence
        self.batch_id = batch_id
        self.pumpkin = pumpkin

        self.client = client
        self._id_attrs = (self.id, self.sequence, self.batch_id, self.pumpkin)

    @classmethod
    def de_json(cls, data, client) -> Optional['StationTracksResult']:
        if not data:
            return None

        data = super(StationTracksResult, cls).de_json(data, client)
        from yandex_music import Id, Sequence
        data['id_'] = Id.de_json(data.get('id_'), client)
        data['sequence'] = Sequence.de_list(data.get('sequence'), client)

        return cls(client=client, **data)
