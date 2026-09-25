from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Station


@model
class WaveSettingsBlock(YandexMusicModel):
    """Класс, представляющий блок настроек волны.

    Note:
        Известные значения поля `type`: `contexts`.

    Attributes:
        type (:obj:`str`, optional): Тип блока.
        items (:obj:`list` из :obj:`yandex_music.Station`, optional): Станции-контексты блока (например, занятия).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    items: Optional[List['Station']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.items)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['WaveSettingsBlock']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.WaveSettingsBlock`: Блок настроек волны.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Station

        cls_data['items'] = Station.de_list(cls_data.get('items'), client)

        return cls(client=client, **cls_data)
