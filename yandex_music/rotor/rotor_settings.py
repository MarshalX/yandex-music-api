from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


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
        mood (:obj:`int`): Настроение (старое).
        energy (:obj:`int`): Энергичное.
        mood_energy (:obj:`str`): Настроение.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        language (:obj:`str`): Язык.
        diversity (:obj:`str`): Разнообразие (треки).
        mood (:obj:`int`, optional): Настроение (старое).
        energy (:obj:`int`, optional): Энергичное.
        mood_energy (:obj:`str`, optional): Настроение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 language: str,
                 diversity: str,
                 mood: Optional[int] = None,
                 energy: Optional[int] = None,
                 mood_energy: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.language = language
        self.diversity = diversity

        self.mood = mood
        self.energy = energy
        self.mood_energy = mood_energy

        self.client = client
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
