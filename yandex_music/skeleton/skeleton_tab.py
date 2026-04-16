from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.skeleton.skeleton_block import SkeletonBlock


@model
class SkeletonTab(YandexMusicModel):
    """Класс, представляющий вкладку скелетона.

    Attributes:
        id (:obj:`str`, optional): Идентификатор вкладки.
        title (:obj:`str`, optional): Заголовок вкладки.
        blocks (:obj:`list` из :obj:`yandex_music.SkeletonBlock`, optional): Блоки вкладки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[str] = None
    title: Optional[str] = None
    blocks: Optional[List['SkeletonBlock']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.title)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['SkeletonTab']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SkeletonTab`: Вкладка скелетона.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.skeleton.skeleton_block import SkeletonBlock

        cls_data['blocks'] = SkeletonBlock.de_list(cls_data.get('blocks'), client)

        return cls(client=client, **cls_data)
