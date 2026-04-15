from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Cover, JSONType
    from yandex_music.wave.wave_agent_entity import WaveAgentEntity


@model
class WaveAgent(YandexMusicModel):
    """Класс, представляющий агента волны.

    Attributes:
        animation_uri (:obj:`str`, optional): URI анимации агента.
        cover (:obj:`yandex_music.Cover`, optional): Обложка агента.
        entity (:obj:`yandex_music.WaveAgentEntity`, optional): Сущность, связанная с агентом.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    animation_uri: Optional[str] = None
    cover: Optional['Cover'] = None
    entity: Optional['WaveAgentEntity'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.animation_uri, self.cover)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['WaveAgent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.WaveAgent`: Агент волны.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Cover
        from yandex_music.wave.wave_agent_entity import WaveAgentEntity

        cls_data['cover'] = Cover.de_json(cls_data.get('cover'), client)
        cls_data['entity'] = WaveAgentEntity.de_json(cls_data.get('entity'), client)

        return cls(client=client, **cls_data)
