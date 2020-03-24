from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Best


class Suggestions(YandexMusicObject):
    """Класс, представляющий подсказки при поиске.

    Attributes:
        best (:obj:`yandex_music.Best`): Лучший результат.
        suggestions (:obj:`list` из :obj:`str`): Список подсказок-дополнений для поискового запроса.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        best (:obj:`yandex_music.Best`): Лучший результат.
        suggestions (:obj:`list` из :obj:`str`): Список подсказок-дополнений для поискового запроса.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 best: Optional['Best'],
                 suggestions: List[str],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.best = best
        self.suggestions = suggestions

        self.client = client
        self._id_attrs = (self.best, self.suggestions)

    def __getitem__(self, item):
        return self.suggestions[item]

    def __iter__(self):
        return iter(self.suggestions)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Suggestions']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Suggestions`: Подсказки при поиске.
        """
        if not data:
            return None

        data = super(Suggestions, cls).de_json(data, client)
        from yandex_music import Best
        data['best'] = Best.de_json(data.get('best'), client)

        return cls(client=client, **data)

