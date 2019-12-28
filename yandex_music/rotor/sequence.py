from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Track

from yandex_music import YandexMusicObject


class Sequence(YandexMusicObject):
    def __init__(self,
                 type_: str,
                 track: Optional['Track'],
                 liked: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.track = track
        self.liked = liked

        self.client = client
        self._id_attrs = (self.type, self.track, self.liked)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Sequence']:
        if not data:
            return None

        data = super(Sequence, cls).de_json(data, client)
        from yandex_music import Track
        data['track'] = Track.de_json(data.get('track'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Sequence']:
        if not data:
            return []

        sequences = list()
        for sequence in data:
            sequences.append(cls.de_json(sequence, client))

        return sequences
