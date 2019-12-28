from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, GeneratedPlaylist, Day

from yandex_music import YandexMusicObject


class Feed(YandexMusicObject):
    def __init__(self,
                 can_get_more_events: bool,
                 pumpkin: bool,
                 is_wizard_passed: bool,
                 generated_playlists: List['GeneratedPlaylist'],
                 headlines: list,
                 today: str,
                 days: List['Day'],
                 next_revision: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.can_get_more_events = can_get_more_events
        self.pumpkin = pumpkin
        self.is_wizard_passed = is_wizard_passed
        self.generated_playlists = generated_playlists
        self.headlines = headlines
        self.today = today
        self.days = days

        self.next_revision = next_revision

        self.client = client
        self._id_attrs = (self.can_get_more_events, self.generated_playlists, self.headlines, self.today, self.days)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Feed']:
        if not data:
            return None

        data = super(Feed, cls).de_json(data, client)
        from yandex_music import GeneratedPlaylist, Day
        data['generated_playlists'] = GeneratedPlaylist.de_list(data.get('generated_playlists'), client)
        data['days'] = Day.de_list(data.get('days'), client)

        return cls(client=client, **data)
