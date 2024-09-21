from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Lyrics, VideoSupplement


@model
class Supplement(YandexMusicModel):
    """Класс, представляющий дополнительную информацию о треке.

    Warning:
        Получение текста из дополнительной информации устарело. Используйте
        :func:`yandex_music.Client.tracks_lyrics`.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор дополнительной информации.
        lyrics (:obj:`yandex_music.Lyrics`): Текст песни.
        videos (:obj:`yandex_music.VideoSupplement`): Видео.
        radio_is_available (:obj:`bool`, optional): Доступно ли радио.
        description (:obj:`str`, optional): Полное описание эпизода подкаста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    lyrics: Optional['Lyrics']
    videos: List['VideoSupplement']
    radio_is_available: Optional[bool] = None
    description: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.lyrics, self.videos)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Supplement']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Supplement`: Дополнительная информация о треке.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Lyrics, VideoSupplement

        cls_data['lyrics'] = Lyrics.de_json(data.get('lyrics'), client)
        cls_data['videos'] = VideoSupplement.de_list(data.get('videos'), client)

        return cls(client=client, **cls_data)  # type: ignore
