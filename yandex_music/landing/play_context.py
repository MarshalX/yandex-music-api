from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, TrackShortOld

from yandex_music import YandexMusicObject


class PlayContext(YandexMusicObject):
    def __init__(self,
                 client_: str,
                 context: str,
                 context_item: str,
                 tracks: List['TrackShortOld'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.client_ = client_
        self.context = context
        self.context_item = context_item
        self.tracks = tracks

        self.client = client
        self._id_attrs = (self.client_, self.context_item, self.context_item, self.tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlayContext']:
        if not data:
            return None

        data = super(PlayContext, cls).de_json(data, client)
        from yandex_music import TrackShortOld
        data['tracks'] = TrackShortOld.de_list(data.get('tracks'), client)

        return cls(client=client, **data)
