from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['SimilarEntityData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SimilarEntityData`: Данные похожей сущности.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.wave.wave import Wave
        from yandex_music.wave.wave_agent import WaveAgent

        cls_data['wave'] = Wave.de_json(cls_data.get('wave'), client)
        cls_data['agent'] = WaveAgent.de_json(cls_data.get('agent'), client)

        return cls(client=client, **cls_data)
