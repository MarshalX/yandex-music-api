from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Day, GeneratedPlaylist, JSONType


@model
class Feed(YandexMusicModel):
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
    headlines: List[str]
    today: str
    days: List['Day']
    next_revision: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.can_get_more_events, self.generated_playlists, self.headlines, self.today, self.days)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Feed']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Feed`: Фид.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Day, GeneratedPlaylist

        cls_data['generated_playlists'] = GeneratedPlaylist.de_list(data.get('generated_playlists'), client)
        cls_data['days'] = Day.de_list(data.get('days'), client)

        return cls(client=client, **cls_data)  # type: ignore
