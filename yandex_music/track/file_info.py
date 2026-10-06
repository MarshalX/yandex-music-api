from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, FileDownloadInfo


@model
class FileInfo(YandexMusicModel):
    """Класс, представляющий информацию о файле трека.

    Attributes:
        download_info (:obj:`yandex_music.FileDownloadInfo`, optional): Информация для загрузки файла.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    download_info: Optional['FileDownloadInfo'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.download_info,)
