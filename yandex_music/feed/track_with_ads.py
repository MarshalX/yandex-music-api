from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Track


@model
class TrackWithAds(YandexMusicModel):
    """Класс, представляющий трек с рекламой.

    Note:
        Поле `type` встречалось только с значением `track`.

    Attributes:
        type (:obj:`str`): Тип TODO.
        track (:obj:`yandex_music.Track`): Трек.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    track: Optional['Track']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.track)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackWithAds']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackWithAds`: Трек с рекламой.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Track

        cls_data['track'] = Track.de_json(data.get('track'), client)

        return cls(client=client, **cls_data)  # type: ignore
