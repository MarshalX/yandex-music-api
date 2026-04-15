from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.track.track import Track


@model
class TrackTrailer(YandexMusicModel):
    """Класс, представляющий трейлер трека.

    Attributes:
        title (:obj:`str`, optional): Заголовок трейлера.
        track (:obj:`yandex_music.Track`, optional): Трек.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    track: Optional['Track'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.track)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackTrailer']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackTrailer`: Трейлер трека.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Track

        cls_data['track'] = Track.de_json(cls_data.get('track'), client)

        return cls(client=client, **cls_data)
