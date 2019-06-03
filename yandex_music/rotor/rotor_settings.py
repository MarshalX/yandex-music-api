from yandex_music import YandexMusicObject


class RotorSettings(YandexMusicObject):
    def __init__(self,
                 language,
                 diversity,
                 mood=None,
                 energy=None,
                 mood_energy=None,
                 client=None,
                 **kwargs):
        self.language = language
        self.diversity = diversity

        self.mood = mood
        self.energy = energy
        self.mood_energy = mood_energy

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(RotorSettings, cls).de_json(data, client)

        return cls(client=client, **data)
