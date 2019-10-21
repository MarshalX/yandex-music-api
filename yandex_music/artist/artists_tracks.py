from yandex_music import YandexMusicObject

class ArtistsTracks(YandexMusicObject):
    """Класс представляющий страницу списка треков артиста

    Attributes:
        tracks (:obj:`yandex_music.Track`): Список треков артиста.
        pager (:obj:`yandex_music.Pager`): Кол-во треков на странице.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        tracks (:obj:`yandex_music.Track`): Список треков артиста.
        pager (:obj:`yandex_music.Pager`): Кол-во треков.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """
    
    def __init__(self,
                 tracks,
                 pager,
                 client=None,
                 **kwargs):
        self.tracks = tracks
        self.pager = pager

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.ArtistsTracks`: Объект класса :class:`yandex_music.ArtistsTracks`.
        """
        if not data:
            return None

        data = super(ArtistsTracks, cls).de_json(data, client)
        from yandex_music import Track, Pager
        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **data)
