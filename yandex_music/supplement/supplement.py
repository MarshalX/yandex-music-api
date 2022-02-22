from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Lyrics, VideoSupplement


@model
class Supplement(YandexMusicObject):
    """Класс, представляющий дополнительную информацию о треке.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор дополнительной информации.
        lyrics (:obj:`yandex_music.Lyrics`): Текст песни.
        videos (:obj:`yandex_music.VideoSupplement`): Видео.
        radio_is_available (:obj:`bool`, optional): Доступно ли радио.
        description (:obj:`str`, optional): Полное описание эпизода подкаста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    lyrics: Optional['Lyrics']
    videos: List['VideoSupplement']
    radio_is_available: bool = None
    description: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.lyrics, self.videos)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Supplement']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Supplement`: Дополнительная информация о треке.
        """
        if not data:
            return None

        data = super(Supplement, cls).de_json(data, client)
        from yandex_music import Lyrics, VideoSupplement

        data['lyrics'] = Lyrics.de_json(data.get('lyrics'), client)
        data['videos'] = VideoSupplement.de_list(data.get('videos'), client)

        return cls(client=client, **data)
