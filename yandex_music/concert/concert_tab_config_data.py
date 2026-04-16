from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.concert.concert_tab_range import ConcertTabRange


@model
class ConcertTabConfigData(YandexMusicModel):
    """Класс, представляющий конфигурацию вкладок концертов.

    Attributes:
        top (:obj:`yandex_music.ConcertTabRange`, optional): Диапазон для блока «Топ».
        feed (:obj:`yandex_music.ConcertTabRange`, optional): Диапазон для ленты концертов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    top: Optional['ConcertTabRange'] = None
    feed: Optional['ConcertTabRange'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.top, self.feed)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ConcertTabConfigData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ConcertTabConfigData`: Конфигурация вкладок концертов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.concert.concert_tab_range import ConcertTabRange

        cls_data['top'] = ConcertTabRange.de_json(cls_data.get('top'), client)
        cls_data['feed'] = ConcertTabRange.de_json(cls_data.get('feed'), client)

        return cls(client=client, **cls_data)
