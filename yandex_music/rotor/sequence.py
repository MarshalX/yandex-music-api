from typing import TYPE_CHECKING, Optional

from yandex_music import JSONType, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Track


@model
class Sequence(YandexMusicModel):
    """Класс, представляющий звено последовательности.

    Note:
        Известные значения поля `type_`: `track`. Возможно есть `ad`.

    Attributes:
        type (:obj:`str`): Тип звена.
        track (:obj:`yandex_music.Track` | :obj:`None`): Трек.
        liked (:obj:`bool`): Связанное ли.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    track: Optional['Track']
    liked: bool
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.track, self.liked)

    @classmethod
    def de_json(cls, data: JSONType, client: 'Client') -> Optional['Sequence']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Sequence`: Звено последовательности.
        """
        if not cls.is_dict_model_data(data):
            return None

        data = cls.cleanup_data(data, client)
        from yandex_music import Track

        data['track'] = Track.de_json(data.get('track'), client)

        return cls(client=client, **data)
