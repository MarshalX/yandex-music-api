from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class CaseForms(YandexMusicModel):
    """Класс, представляющий склонение имени.

    Attributes:
        nominative (:obj:`str`): Именительный.
        genitive (:obj:`str`): Родительный.
        dative (:obj:`str`): Дательный.
        accusative (:obj:`str`): Винительный.
        instrumental (:obj:`str`): Творительный.
        prepositional (:obj:`str`): Предложный.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    nominative: str
    genitive: str
    dative: str
    accusative: str
    instrumental: str
    prepositional: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (
            self.nominative,
            self.genitive,
            self.dative,
            self.accusative,
            self.instrumental,
            self.prepositional,
        )
