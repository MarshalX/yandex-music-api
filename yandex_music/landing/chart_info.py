from typing import TYPE_CHECKING, Optional

from yandex_music import ChartInfoMenu, Playlist, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


@model
class ChartInfo(YandexMusicModel):
    """Класс, представляющий чарт.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор блока.
        type (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        menu (:obj:`yandex_music.ChartInfoMenu`, optional): Меню TODO.
        chart (:obj:`yandex_music.Playlist`, optional): Плейлист.
        chart_description (:obj:`str`, optional): Описание.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    type: str
    type_for_from: str
    title: str
    menu: Optional['ChartInfoMenu']
    chart: Optional['Playlist']
    chart_description: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ChartInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ChartInfo`: Чарт.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        cls_data['chart'] = Playlist.de_json(data.get('chart'), client)
        cls_data['menu'] = ChartInfoMenu.de_json(data.get('menu'), client)

        return cls(client=client, **cls_data)  # type: ignore
