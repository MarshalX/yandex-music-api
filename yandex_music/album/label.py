from yandex_music import YandexMusicObject


class Label(YandexMusicObject):
    """Класс, представляющий лейбл альбома.
    
        Attributes:
            id (:obj:`int`): Идентификатор альбома.
            name (:obj:`str`): Название альбома.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.
        Args:
            id (:obj:`int`): Идентификатор альбома.
            name (:obj:`str`): Название альбома.
            client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
                Yandex Music.
            **kwargs: Произвольные ключевые аргументы полученные от API.
        """
    def __init__(self,
                 id,
                 name,
                 client=None,
                 **kwargs):
        self.id = id
        self.name = name

        self.client = client
        self._id_attrs = (self.id, self.name)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.
        
             Args:
                 data (:obj:`dict`): Поля и значения десериализуемого объекта.
                 client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                     Music.
             Returns:
                 :obj:`yandex_music.Label`: Объект класса :class:`yandex_music.Label`.
        """
        if not data:
            return None

        data = super(Label, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.
        
            Args:
                data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
                client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                    Music.
            Returns:
                :obj:`list` из :obj:`yandex_music.Label`: Список объектов класса :class:`yandex_music.Label`.
        """
        if not data:
            return []

        labels = list()
        for label in data:
            labels.append(cls.de_json(label, client))

        return labels
