from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.concert.concert_tab_config_data import ConcertTabConfigData


@model
class ConcertTabConfig(YandexMusicModel):
    """Класс, представляющий конфигурацию вкладок ленты концертов.

    Attributes:
        config (:obj:`yandex_music.ConcertTabConfigData`, optional): Конфигурация вкладок концертов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    config: Optional['ConcertTabConfigData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.config,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ConcertTabConfig']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ConcertTabConfig`: Конфигурация вкладок концертов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.concert.concert_tab_config_data import ConcertTabConfigData

        cls_data['config'] = ConcertTabConfigData.de_json(cls_data.get('config'), client)

        return cls(client=client, **cls_data)
