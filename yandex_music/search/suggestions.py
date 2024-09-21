from typing import TYPE_CHECKING, Iterable, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Best, ClientType, JSONType


@model
class Suggestions(YandexMusicModel):
    """Класс, представляющий подсказки при поиске.

    Attributes:
        best (:obj:`yandex_music.Best`): Лучший результат.
        suggestions (:obj:`list` из :obj:`str`): Список подсказок-дополнений для поискового запроса.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    best: Optional['Best']
    suggestions: List[str]
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.best, self.suggestions)

    def __getitem__(self, item: int) -> str:
        return self.suggestions[item]

    def __iter__(self) -> Iterable[str]:
        return iter(self.suggestions)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Suggestions']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Suggestions`: Подсказки при поиске.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Best

        cls_data['best'] = Best.de_json(data.get('best'), client)

        return cls(client=client, **cls_data)  # type: ignore
