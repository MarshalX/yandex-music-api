from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, GeneratedPlaylist, Day


@model
class Feed(YandexMusicObject):
    """Класс, представляющий фид.

    Note:
        Несмотря на то, что days это :obj:`list`, обычно возвращается только один день - текущий.

    Attributes:
        can_get_more_events (:obj:`bool`): Можно ли получить больше событий.
        pumpkin (:obj:`bool`): Хэллоуин.
        is_wizard_passed (:obj:`bool`): TODO.
        generated_playlists (:obj:`list` из :obj:`yandex_music.GeneratedPlaylist`): Сгенерированные плейлисты.
        headlines (:obj:`list` из :obj:`str`): Заголовки.
        today (:obj:`str`): Сегодняшняя дата в формате YYYY-MM-DD.
        days (:obj:`list` из :obj:`yandex_music.Day`): Дни.
        next_revision (:obj:`str`, optional): Дата следующих изменений в формате YYYY-MM-DD.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    can_get_more_events: bool
    pumpkin: bool
    is_wizard_passed: bool
    generated_playlists: List['GeneratedPlaylist']
    headlines: list
    today: str
    days: List['Day']
    next_revision: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.can_get_more_events, self.generated_playlists, self.headlines, self.today, self.days)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Feed']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Feed`: Фид.
        """
        if not data:
            return None

        data = super(Feed, cls).de_json(data, client)
        from yandex_music import GeneratedPlaylist, Day

        data['generated_playlists'] = GeneratedPlaylist.de_list(data.get('generated_playlists'), client)
        data['days'] = Day.de_list(data.get('days'), client)

        return cls(client=client, **data)
