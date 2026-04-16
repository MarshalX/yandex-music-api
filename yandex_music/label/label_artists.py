from typing import TYPE_CHECKING, Iterator, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType, JSONType, Pager


@model
class LabelArtists(YandexMusicModel):
    """Класс, представляющий страницу списка артистов лейбла.

    Attributes:
        artists (:obj:`list` из :obj:`yandex_music.Artist`): Список артистов лейбла.
        pager (:obj:`yandex_music.Pager`, optional): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artists: List['Artist']
    pager: Optional['Pager']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.pager, self.artists)

    def __getitem__(self, item: int) -> 'Artist':
        return self.artists[item]

    def __iter__(self) -> Iterator['Artist']:
        return iter(self.artists)

    def __len__(self) -> int:
        return len(self.artists)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['LabelArtists']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LabelArtists`: Страница списка артистов лейбла.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist, Pager

        cls_data['artists'] = Artist.de_list(cls_data.get('artists'), client)
        cls_data['pager'] = Pager.de_json(cls_data.get('pager'), client)

        return cls(client=client, **cls_data)
