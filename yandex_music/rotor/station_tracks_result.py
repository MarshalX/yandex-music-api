from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Id, Sequence


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
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.StationTracksResult`: Объект класса :class:`yandex_music.StationTracksResult`.
        """
        if not data:
            return None

        data = super(StationTracksResult, cls).de_json(data, client)
        from yandex_music import Id, Sequence
        data['id_'] = Id.de_json(data.get('id_'), client)
        data['sequence'] = Sequence.de_list(data.get('sequence'), client)

        return cls(client=client, **data)
