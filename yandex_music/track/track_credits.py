from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.track.track_credit import TrackCredit


@model
class TrackCredits(YandexMusicModel):
    """Класс, представляющий список участников создания трека.

    Attributes:
        credits (:obj:`list` из :obj:`yandex_music.TrackCredit`, optional): Список участников.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    credits: Optional[List['TrackCredit']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.credits,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackCredits']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackCredits`: Список участников создания трека.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.track.track_credit import TrackCredit

        cls_data['credits'] = TrackCredit.de_list(cls_data.get('credits'), client)

        return cls(client=client, **cls_data)
