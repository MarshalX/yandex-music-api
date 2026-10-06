from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model
from yandex_music.utils.decrypt import decrypt_track
from yandex_music.utils.request_base import default_timeout

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.utils.request_base import TimeoutType


@model
class FileDownloadInfo(YandexMusicModel):
    """Класс, представляющий информацию о файле трека для загрузки.

    Note:
        Известные значения поля `quality`: `lossless`, `hq`, `nq`.

        Известные значения поля `codec`: `flac`, `flac-mp4`, `aac-mp4`, `he-aac-mp4`, `aac`, `he-aac`, `mp3`.
        Кодеки с суффиксом `-mp4` поставляются в контейнере MP4.

        Известные значения поля `transport`: `raw`, `encraw`. При `encraw` файл зашифрован ключом из поля `key`,
        методы загрузки расшифровывают его автоматически.

        Для `flac-mp4` поле `bitrate` равно `0`.

    Attributes:
        track_id (:obj:`str`): Уникальный идентификатор трека из запроса.
        quality (:obj:`str`): Качество.
        codec (:obj:`str`): Кодек.
        bitrate (:obj:`int`): Битрейт в кбит/с.
        transport (:obj:`str`): Способ доставки файла.
        url (:obj:`str`): Ссылка на файл.
        urls (:obj:`list` из :obj:`str`): Ссылки на файл на разных серверах.
        real_id (:obj:`str`, optional): Уникальный идентификатор трека.
        gain (:obj:`bool`, optional): Усиление.
        key (:obj:`str`, optional): Ключ расшифровки в шестнадцатеричном виде для `encraw`.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track_id: str
    quality: str
    codec: str
    bitrate: int
    transport: str
    url: str
    urls: List[str]
    real_id: Optional[str] = None
    gain: Optional[bool] = None
    key: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track_id, self.quality, self.codec, self.transport, self.url)

    def _decrypt(self, data: bytes) -> bytes:
        if self.transport == 'encraw' and self.key is not None and self.key != '':
            return decrypt_track(data, self.key)

        return data

    def download_bytes(self, timeout: 'TimeoutType' = default_timeout) -> bytes:
        """Загрузка трека и возврат в виде байтов.

        Note:
            Файл в `encraw` расшифровывается.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Время ожидания ответа сервера в секундах. Ограничивает
                ожидание соединения и каждой порции данных, а не всю загрузку. По умолчанию используется значение
                клиента.

        Returns:
            :obj:`bytes`: Трек в виде байтов.
        """
        assert self.valid_client(self.client)
        return self._decrypt(self.client.request.retrieve(self.url, timeout=timeout))

    async def download_bytes_async(self, timeout: 'TimeoutType' = default_timeout) -> bytes:
        """Загрузка трека и возврат в виде байтов.

        Note:
            Файл в `encraw` расшифровывается.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Время ожидания в секундах. Ограничивает всё время запроса
                целиком, включая загрузку файла. По умолчанию используется значение клиента.

        Returns:
            :obj:`bytes`: Трек в виде байтов.
        """
        assert self.valid_async_client(self.client)
        return self._decrypt(await self.client.request.retrieve(self.url, timeout=timeout))

    def download(self, filename: str, timeout: 'TimeoutType' = default_timeout) -> None:
        """Загрузка трека.

        Note:
            Файл в `encraw` расшифровывается. Контейнер не меняется: `flac-mp4` и `aac-mp4` сохраняются как MP4.

        Args:
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
            timeout (:obj:`int` | :obj:`float`, optional): Время ожидания ответа сервера в секундах. Ограничивает
                ожидание соединения и каждой порции данных, а не всю загрузку. По умолчанию используется значение
                клиента.
        """
        data = self.download_bytes(timeout)
        with open(filename, 'wb') as f:
            _ = f.write(data)

    async def download_async(self, filename: str, timeout: 'TimeoutType' = default_timeout) -> None:
        """Загрузка трека.

        Note:
            Файл в `encraw` расшифровывается. Контейнер не меняется: `flac-mp4` и `aac-mp4` сохраняются как MP4.

        Args:
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
            timeout (:obj:`int` | :obj:`float`, optional): Время ожидания в секундах. Ограничивает всё время запроса
                целиком, включая загрузку файла. По умолчанию используется значение клиента.
        """
        import aiofiles

        data = await self.download_bytes_async(timeout)
        async with aiofiles.open(filename, 'wb') as f:
            await f.write(data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_bytes`
    downloadBytes = download_bytes
    #: Псевдоним для :attr:`download_bytes_async`
    downloadBytesAsync = download_bytes_async
    #: Псевдоним для :attr:`download_async`
    downloadAsync = download_async
