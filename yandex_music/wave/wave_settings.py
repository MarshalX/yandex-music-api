from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Restrictions, WaveDefaultStation, WaveSettingsBlock


@model
class WaveSettings(YandexMusicModel):
    """Класс, представляющий настройки волны.

    Note:
        Значения из `setting_restrictions` можно передавать как сиды сессии радио
        (поле :attr:`yandex_music.Value.serialized_seed`, например, `settingDiversity:favorite`).

    Attributes:
        default_station (:obj:`yandex_music.WaveDefaultStation`, optional): Станция волны по умолчанию.
        blocks (:obj:`list` из :obj:`yandex_music.WaveSettingsBlock`, optional): Блоки настроек.
        setting_restrictions (:obj:`yandex_music.Restrictions`, optional): Доступные значения настроек волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    default_station: Optional['WaveDefaultStation'] = None
    blocks: Optional[List['WaveSettingsBlock']] = None
    setting_restrictions: Optional['Restrictions'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.default_station, self.blocks, self.setting_restrictions)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['WaveSettings']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.WaveSettings`: Настройки волны.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Restrictions, WaveDefaultStation, WaveSettingsBlock

        cls_data['default_station'] = WaveDefaultStation.de_json(cls_data.get('default_station'), client)
        cls_data['blocks'] = WaveSettingsBlock.de_list(cls_data.get('blocks'), client)
        cls_data['setting_restrictions'] = Restrictions.de_json(cls_data.get('setting_restrictions'), client)

        return cls(client=client, **cls_data)
