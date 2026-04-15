from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.foreign_agent import ForeignAgent


@model
class Disclaimer(YandexMusicModel):
    """Класс, представляющий дисклеймер.

    Attributes:
        foreign_agent (:obj:`yandex_music.ForeignAgent`, optional): Информация о статусе иноагента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    foreign_agent: Optional['ForeignAgent'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.foreign_agent,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Disclaimer']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Disclaimer`: Дисклеймер.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.foreign_agent import ForeignAgent

        cls_data['foreign_agent'] = ForeignAgent.de_json(cls_data.get('foreign_agent'), client)

        return cls(client=client, **cls_data)
