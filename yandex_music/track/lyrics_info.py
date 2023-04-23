from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class LyricsInfo(YandexMusicObject):
    """Класс, описывающий доступные тексты трека.

    Attributes:
        has_available_sync_lyrics (:obj:`bool`): Наличие синхронизированного текста.
        has_available_text_lyrics (:obj:`bool`): Наличие текста трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    has_available_sync_lyrics: bool
    has_available_text_lyrics: bool
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.has_available_sync_lyrics, self.has_available_text_lyrics)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['LyricsInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LyricsInfo`: Типы доступных текстов трека.
        """
        if not data:
            return None

        data = super(LyricsInfo, cls).de_json(data, client)

        return cls(client=client, **data)
