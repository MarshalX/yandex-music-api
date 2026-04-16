from dataclasses import field
from typing import TYPE_CHECKING, Dict, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, ExperimentDetail, JSONType


@model
class ExperimentsDetails(YandexMusicModel):
    """Класс, представляющий детальные значения экспериментальных функций аккаунта.

    Note:
        API возвращает словарь, где ключи — названия экспериментов (например,
        ``AliceTest`` или ``3dsRubilnik``), а значения — объекты
        :class:`yandex_music.ExperimentDetail` с названием выбранной группы и её
        параметрами. Набор экспериментов заранее неизвестен и может меняться от
        запроса к запросу, поэтому хранится в :attr:`experiments`.

    Attributes:
        experiments (:obj:`dict` из :obj:`str` в :obj:`yandex_music.ExperimentDetail`):
            Словарь экспериментов, ключ — название эксперимента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    experiments: Dict[str, 'ExperimentDetail'] = field(default_factory=dict)
    client: Optional['ClientType'] = None

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ExperimentsDetails']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ExperimentsDetails`: Детали экспериментов аккаунта.
        """
        if not cls.is_dict_model_data(data):
            return None

        from yandex_music import ExperimentDetail

        experiments: Dict[str, 'ExperimentDetail'] = {}
        for name, entry in data.items():
            detail = ExperimentDetail.de_json(entry, client)
            if detail is not None:
                experiments[name] = detail

        return cls(client=client, experiments=experiments)
