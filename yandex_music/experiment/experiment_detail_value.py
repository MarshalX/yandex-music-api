from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model
from yandex_music.utils.normalize import _normalize_key

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


@model
class ExperimentDetailValue(YandexMusicModel):
    """Класс, представляющий значение (конфигурацию) эксперимента.

    Note:
        Для каждого эксперимента API возвращает свой набор полей конфигурации:
        флаги, идентификаторы, пороговые значения, списки, вложенные словари и т. п.
        Универсальное поле у всех экспериментов одно — :attr:`title`; оно совпадает
        с :attr:`yandex_music.ExperimentDetail.group`.

        Остальные поля сохраняются в :obj:`__dict__` экземпляра при десериализации
        и доступны как обычные атрибуты и через :meth:`to_dict`. Их набор и типы
        зависят от конкретного эксперимента и не типизируются.

    Attributes:
        title (:obj:`str`, optional): Название/идентификатор группы эксперимента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ExperimentDetailValue']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ExperimentDetailValue`: Значение эксперимента.
        """
        if not cls.is_dict_model_data(data):
            return None

        raw_title = data.get('title')
        title = raw_title if isinstance(raw_title, str) else None
        instance = cls(client=client, title=title)

        for key, value in data.items():
            normalized = _normalize_key(key)
            if normalized in ('title', 'client'):
                continue
            instance.__dict__[normalized] = value

        return instance
