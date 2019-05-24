from yandex_music import YandexMusicObject


class PersonalPlaylistsData(YandexMusicObject):
    def __init__(self,
                 is_wizard_passed,
                 client=None,
                 **kwargs):
        self.is_wizard_passed = is_wizard_passed

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PersonalPlaylistsData, cls).de_json(data, client)

        return cls(client=client, **data)
