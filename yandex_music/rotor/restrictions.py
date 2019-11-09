from yandex_music import YandexMusicObject, Enum, DiscreteScale


de_json = {
    'enum': Enum.de_json,
    'discrete-scale': DiscreteScale.de_json
}


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
        self._id_attrs = (self.language, self.diversity)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Restrictions, cls).de_json(data, client)

        for key, value in data.items():
            data[key] = de_json.get(value.get('type'))(value, client)

        return cls(client=client, **data)
