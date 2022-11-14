from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model


if TYPE_CHECKING:
    from yandex_music import Client, LyricsMajor


@model
class TrackLyrics(YandexMusicObject):
    """TODO"""

    download_url: str
    lyric_id: int
    external_lyric_id: str
    writers: List[str]
    major: 'LyricsMajor'
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (
            self.lyric_id,
            self.external_lyric_id,
        )

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TrackLyrics']:
        """TODO"""
        if not data:
            return None

        data = super(TrackLyrics, cls).de_json(data, client)
        from yandex_music import LyricsMajor

        data['major'] = LyricsMajor.de_json(data.get('major'), client)

        return cls(client=client, **data)
