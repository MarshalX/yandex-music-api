from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Chart, ClientType, JSONType, Track


@model
class ChartItem(YandexMusicModel):
    """Класс, представляющий трек в чарте.

    Attributes:
        track (:obj:`yandex_music.Track` | :obj:`None`): Трек.
        chart (:obj:`yandex_music.Chart` | :obj:`None`): Элемент чарт.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track: Optional['Track']
    chart: Optional['Chart']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track, self.chart)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ChartItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ChartItem`: Трек в чарте.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Chart, Track

        cls_data['track'] = Track.de_json(data.get('track'), client)
        cls_data['chart'] = Chart.de_json(data.get('chart'), client)

        return cls(client=client, **cls_data)  # type: ignore
