from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, TrackId


@model
class TrackShortOld(YandexMusicModel):
    """Класс, представляющий сокращённую версию трека.

    Note:
        Данная версия менее богата полями и найдена позже первой, поэтому была принята как за старую версию.

        Другая версия сокращённого трека: :class:`yandex_music.TrackShort`.

    Attributes:
        track_id (:obj:`yandex_music.TrackId`): Уникальный идентификатор трека.
        timestamp (:obj:`str`): Дата TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track_id: Optional['TrackId']
    timestamp: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track_id,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackShortOld']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackShortOld`: Сокращённая версия трека или :obj:`None`.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import TrackId

        cls_data['track_id'] = TrackId.de_json(data.get('track_id'), client)

        return cls(client=client, **cls_data)  # type: ignore
