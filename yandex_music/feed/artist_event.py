from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType, JSONType, Track


@model
class ArtistEvent(YandexMusicModel):
    """Класс, представляющий артиста в событии фида.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Треки.
        similar_to_artists_from_history (:obj:`list` из :obj:`yandex_music.Artist`): Похожие артисты из истории.
        subscribed (:obj:`bool`): Подписан ли на событие.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist']
    tracks: List['Track']
    similar_to_artists_from_history: List['Artist']
    subscribed: Optional['bool'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist, self.tracks, self.similar_to_artists_from_history)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistEvent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistEvent`: Артист из события фида.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist, Track

        cls_data['artist'] = Artist.de_json(data.get('artist'), client)
        cls_data['tracks'] = Track.de_list(data.get('tracks'), client)
        cls_data['similar_to_artists_from_history'] = Artist.de_list(
            data.get('similar_to_artists_from_history'), client
        )

        return cls(client=client, **cls_data)  # type: ignore
