from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, TrackShortOld


@model
class PlayContextsData(YandexMusicModel):
    """Класс, представляющий данные проигрываемого контекста.

    Attributes:
        other_tracks (:obj:`list` из :obj:`yandex_music.TrackShortOld`): Другие треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    other_tracks: List['TrackShortOld']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.other_tracks,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['PlayContextsData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlayContextsData`: Данные проигрываемого контекста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import TrackShortOld

        cls_data['other_tracks'] = TrackShortOld.de_list(data.get('other_tracks'), client)

        return cls(client=client, **cls_data)  # type: ignore
