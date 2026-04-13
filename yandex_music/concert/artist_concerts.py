from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.concert.concert import Concert


@model
class ArtistConcerts(YandexMusicModel):
    """Класс, представляющий список концертов артиста.

    Attributes:
        artist_title (:obj:`str`, optional): Название артиста.
        concerts (:obj:`list` из :obj:`yandex_music.Concert`): Список концертов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist_title: Optional[str] = None
    concerts: List['Concert'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist_title, self.concerts)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistConcerts']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistConcerts`: Список концертов артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.concert.concert import Concert

        cls_data['concerts'] = Concert.de_list(cls_data.get('concerts'), client)

        return cls(client=client, **cls_data)  # type: ignore
