from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Images(YandexMusicObject):
    """Класс, представляющий изображение жанра.

    Attributes:
        _208x208 (:obj:`str`, optional): Ссылка на изображение размером 208 на 208.
        _300x300 (:obj:`str`, optional): Ссылка на изображение размером 300 на 300.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    _208x208: Optional[str] = None
    _300x300: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self._208x208, self._300x300)

    def download_208x208(self, filename: str) -> None:
        """Загрузка изображения 208x208.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        self.client.request.download(self._208x208, filename)

    def download_300x300(self, filename: str) -> None:
        """Загрузка изображения 300x300.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        self.client.request.download(self._300x300, filename)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Images']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Images`: Изображение жанра.
        """
        if not data:
            return None

        data = super(Images, cls).de_json(data, client)

        return cls(client=client, **data)
