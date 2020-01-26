from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Images(YandexMusicObject):
    def __init__(self,
                 _208x208: Optional[str] = None,
                 _300x300: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self._208x208 = _208x208
        self._300x300 = _300x300

        self.client = client

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
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Images`: Объект класса :class:`yandex_music.Images`.
        """
        if not data:
            return None

        data = super(Images, cls).de_json(data, client)

        return cls(client=client, **data)

