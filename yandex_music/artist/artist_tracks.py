from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Track, Pager


class ArtistTracks(YandexMusicObject):
    """Класс, представляющий страницу списка треков артиста.

    Attributes:
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Список треков артиста.
        pager (:obj:`yandex_music.Pager`): Пагинатор.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Список треков артиста.
        pager (:obj:`yandex_music.Pager`): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 tracks: List['Track'],
                 pager: Optional['Pager'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.tracks = tracks
        self.pager = pager

        self.client = client
        self._id_attrs = (self.pager, self.tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ArtistTracks']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistsTracks`: Страница списка треков артиста.
        """
        if not data:
            return None

        data = super(ArtistTracks, cls).de_json(data, client)
        from yandex_music import Track, Pager
        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **data)
