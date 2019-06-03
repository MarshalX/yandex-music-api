from yandex_music import YandexMusicObject


class Restrictions(YandexMusicObject):
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

        data = super(Restrictions, cls).de_json(data, client)
        from yandex_music import Enum, DiscreteScale
        for key, value in data.items():
            restriction_type = data[key].get('type')

            data[key] = Enum.de_json(data[key], client) if restriction_type == 'enum'\
                else DiscreteScale.de_json(data[key], client)

        return cls(client=client, **data)
