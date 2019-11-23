from yandex_music import YandexMusicObject


class PlaylistAbsence(YandexMusicObject):
    """Класс представляющий причину отсутствия плейлиста.

    Attributes:
        kind (:obj:`int`): Уникальный идентификатор плейлиста.
        reason (:obj:`str`): Причина отсутствия.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        kind (:obj:`int`): Уникальный идентификатор плейлиста.
        reason (:obj:`str`): Причина отсутствия.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 kind,
                 reason,
                 client=None,
                 **kwargs):
        self.kind = kind
        self.reason = reason

        self.client = client
        self._id_attrs = (self.kind, self.reason)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.PlaylistAbsence`: Объект класса :class:`yandex_music.PlaylistAbsence`.
        """
        if not data:
            return None

        data = super(PlaylistAbsence, cls).de_json(data, client)

        return cls(client=client, **data)
