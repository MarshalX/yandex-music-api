from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, ShotType


@model
class ShotData(YandexMusicObject):
    """Класс, представляющий основную информацию о шоте.

    Attributes:
        cover_uri (:obj:`str`): Ссылка на обложку шота (иконка Алисы).
        mds_url (:obj:`str`): Ссылка на аудиоверсию шота в озвучке от Алисы.
        shot_text (:obj:`str`): Текстовая версия шота.
        shot_type (:obj:`yandex_music.ShotType`): Тип шота.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    cover_uri: str
    mds_url: str
    shot_text: str
    shot_type: 'ShotType'
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.cover_uri, self.mds_url, self.shot_text, self.shot_type)

    def download_cover(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(f'https://{self.cover_uri.replace("%%", size)}', filename)

    async def download_cover_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        await self.client.request.download(f'https://{self.cover_uri.replace("%%", size)}', filename)

    def download_mds(self, filename: str) -> None:
        """Загрузка аудиоверсии шота.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        self.client.request.download(self.mds_url, filename)

    async def download_mds_async(self, filename: str) -> None:
        """Загрузка аудиоверсии шота.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        await self.client.request.download(self.mds_url, filename)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ShotData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ShotData`: Основная информация о шоте.
        """
        if not data:
            return None

        data = super(ShotData, cls).de_json(data, client)
        from yandex_music import ShotType

        data['shot_type'] = ShotType.de_json(data.get('shot_type'), client)

        return cls(client=client, **data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_cover`
    downloadCover = download_cover
    #: Псевдоним для :attr:`download_cover_async`
    downloadCoverAsync = download_cover_async
    #: Псевдоним для :attr:`download_mds`
    downloadMds = download_mds
    #: Псевдоним для :attr:`download_mds_async`
    downloadMdsAsync = download_mds_async
