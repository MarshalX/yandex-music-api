from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, ExperimentDetailValue, JSONType


@model
class ExperimentDetail(YandexMusicModel):
    """Класс, представляющий один эксперимент в детализированном ответе.

    Note:
        Значение поля :attr:`group` совпадает с :attr:`value.title
        <yandex_music.ExperimentDetailValue.title>`. Поле :attr:`value`
        содержит дополнительные параметры конфигурации выбранной группы эксперимента.

    Attributes:
        group (:obj:`str`, optional): Название выбранной группы эксперимента.
        value (:obj:`yandex_music.ExperimentDetailValue`, optional): Конфигурация
            выбранной группы эксперимента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    group: Optional[str] = None
    value: Optional['ExperimentDetailValue'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.group, self.value)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ExperimentDetail']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ExperimentDetail`: Описание эксперимента.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import ExperimentDetailValue

        cls_data['value'] = ExperimentDetailValue.de_json(cls_data.get('value'), client)

        return cls(client=client, **cls_data)
