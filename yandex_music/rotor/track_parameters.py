from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Fade, JSONType


@model
class TrackParameters(YandexMusicModel):
    """Класс, представляющий параметры трека в радио.

    Attributes:
        bpm (:obj:`int`, optional): Темп трека (ударов в минуту).
        energy (:obj:`float`, optional): Энергичность трека.
        hue (:obj:`float`, optional): Оттенок трека.
        user_collection_hue (:obj:`int`, optional): Оттенок коллекции пользователя.
        mix_fade (:obj:`yandex_music.Fade`, optional): Параметры затухания трека при сведении.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    bpm: Optional[int] = None
    energy: Optional[float] = None
    hue: Optional[float] = None
    user_collection_hue: Optional[int] = None
    mix_fade: Optional['Fade'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.bpm, self.energy, self.hue)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackParameters']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackParameters`: Параметры трека в радио.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Fade

        cls_data['mix_fade'] = Fade.de_json(cls_data.get('mix_fade'), client)

        return cls(client=client, **cls_data)
