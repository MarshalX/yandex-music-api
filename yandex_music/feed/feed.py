from datetime import datetime

from yandex_music import YandexMusicObject


class Feed(YandexMusicObject):
    def __init__(self,
                 can_get_more_events,
                 pumpkin,
                 is_wizard_passed,
                 generated_playlists,
                 headlines,
                 today,
                 days,
                 next_revision=None,
                 client=None,
                 **kwargs):
        self.can_get_more_events = can_get_more_events
        self.pumpkin = pumpkin
        self.is_wizard_passed = is_wizard_passed
        self.generated_playlists = generated_playlists
        self.headlines = headlines
        self.today = datetime.fromisoformat(today)
        self.days = days

        self.next_revision = datetime.fromisoformat(next_revision) if next_revision else next_revision

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Feed, cls).de_json(data, client)
        from yandex_music import GeneratedPlaylist, Day
        data['generated_playlists'] = GeneratedPlaylist.de_list(data.get('generated_playlists'), client)
        data['days'] = Day.de_list(data.get('days'), client)

        return cls(client=client, **data)
