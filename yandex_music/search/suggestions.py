from typing import TYPE_CHECKING, Iterator, List, Optional

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Best, ClientType


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

    @override
    def __getitem__(self, item: int) -> str:
        return self.suggestions[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self.suggestions)
