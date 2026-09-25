from typing import TYPE_CHECKING, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, SessionPlayable


@model
class SessionEvent(YandexMusicModel):
    """Класс, представляющий событие обратной связи сессии радио.

    Note:
        Известные значения поля `type`: `radioStarted`, `trackStarted`, `trackFinished`, `skip`, `skipFailed`,
        `like`, `unlike`, `dislike`, `undislike`, `playableItemStarted`, `playableItemFinished`,
        `playableItemSkip`, `playableItemLike`, `playableItemUnlike`, `playableItemDislike`,
        `playableItemUndislike`, `combinedQueueStarted`, `ad`.

        Поле `timestamp` обязательно для всех событий. Событиям `trackStarted`, `trackFinished`, `skip`, `like`,
        `unlike`, `dislike`, `undislike` нужен `track_id`; событиям `playableItem*` нужен `playable`.
        Событиям `trackFinished`, `skip`, `dislike`, `playableItemFinished`, `playableItemSkip`,
        `playableItemDislike` нужен `total_played_seconds`.

        События лайков и дизлайков влияют только на рекомендации и не изменяют коллекцию пользователя.

    Attributes:
        type (:obj:`str`): Тип события.
        timestamp (:obj:`str` | :obj:`int` | :obj:`float`): Время события. Рекомендуется строка в формате
            ISO 8601 (например, `2024-01-01T12:00:00.000Z`).
        track_id (:obj:`str`, optional): Уникальный идентификатор трека (`id` или `id:album_id`).
        total_played_seconds (:obj:`int` | :obj:`float`, optional): Сколько секунд трека было проиграно.
        playable (:obj:`yandex_music.SessionPlayable`, optional): Проигрываемый объект.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    timestamp: Union[str, int, float]
    track_id: Optional[str] = None
    total_played_seconds: Optional[Union[int, float]] = None
    playable: Optional['SessionPlayable'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.timestamp, self.track_id, self.playable)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['SessionEvent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SessionEvent`: Событие обратной связи сессии радио.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import SessionPlayable

        cls_data['playable'] = SessionPlayable.de_json(cls_data.get('playable'), client)

        return cls(client=client, **cls_data)
