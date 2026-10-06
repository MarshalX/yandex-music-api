from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.wave.wave import Wave
    from yandex_music.wave.wave_agent import WaveAgent


@model
class SimilarEntityData(YandexMusicModel):
    """Класс, представляющий данные похожей сущности.

    Attributes:
        wave (:obj:`yandex_music.Wave`, optional): Волна.
        agent (:obj:`yandex_music.WaveAgent`, optional): Агент волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    wave: Optional['Wave'] = None
    agent: Optional['WaveAgent'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.wave, self.agent)
