from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class RotorSettings(YandexMusicObject):
    """Класс, представляющий настройки станции.

    Note:
        Поля `energy`, `mood` используются в старых настройках (`settings1`).

        Значения `mood_energy`: `fun`, `active`, `calm`, `sad`, `all`.

        Значения `diversity`: `favorite`, `popular`, `discover`, `default`.

        Значения `language`: `not-russian`, `russian`, `any`.

    Attributes:
        language (:obj:`str`): Язык.
        diversity (:obj:`str`): Разнообразие (треки).
        mood (:obj:`int`, optional): Настроение (старое).
        energy (:obj:`int`, optional): Энергичное.
        mood_energy (:obj:`str`, optional): Настроение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    language: str
    diversity: str
    mood: Optional[int] = None
    energy: Optional[int] = None
    mood_energy: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.language, self.diversity)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['RotorSettings']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.RotorSettings`: Настройки станции.
        """
        if not data:
            return None

        data = super(RotorSettings, cls).de_json(data, client)

        return cls(client=client, **data)
