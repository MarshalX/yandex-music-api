from typing import TYPE_CHECKING, Optional

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, FileDownloadInfo, JSONType


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

    @classmethod
    @override
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['FileInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.FileInfo`: Информация о файле трека.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import FileDownloadInfo

        cls_data['download_info'] = FileDownloadInfo.de_json(cls_data.get('download_info'), client)

        return cls(client=client, **cls_data)
