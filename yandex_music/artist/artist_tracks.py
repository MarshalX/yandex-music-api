from typing import TYPE_CHECKING, Iterator, List, Optional

from yandex_music import JSONType, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Pager, Track


@model
class ArtistTracks(YandexMusicModel):
    """Класс, представляющий страницу списка треков артиста.

    Attributes:
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Список треков артиста.
        pager (:obj:`yandex_music.Pager`): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tracks: List['Track']
    pager: Optional['Pager']
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.pager, self.tracks)

    def __getitem__(self, item: int) -> 'Track':
        return self.tracks[item]

    def __iter__(self) -> Iterator['Track']:
        return iter(self.tracks)

    def __len__(self) -> int:
        return len(self.tracks)

    @classmethod
    def de_json(cls, data: JSONType, client: 'Client') -> Optional['ArtistTracks']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistsTracks`: Страница списка треков артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        data = cls.cleanup_data(data, client)
        from yandex_music import Pager, Track

        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **data)
