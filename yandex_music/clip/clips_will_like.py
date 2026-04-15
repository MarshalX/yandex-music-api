from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.clip.clip import Clip
    from yandex_music.pager import Pager


@model
class ClipsWillLike(YandexMusicModel):
    """Класс, представляющий подборку рекомендуемых клипов.

    Attributes:
        clips (:obj:`list` из :obj:`yandex_music.Clip`, optional): Список клипов.
        pager (:obj:`yandex_music.Pager`, optional): Пагинация.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    clips: Optional[List['Clip']] = None
    pager: Optional['Pager'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.clips, self.pager)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ClipsWillLike']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ClipsWillLike`: Подборка рекомендуемых клипов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Pager
        from yandex_music.clip.clip import Clip

        cls_data['clips'] = Clip.de_list(cls_data.get('clips'), client)
        cls_data['pager'] = Pager.de_json(cls_data.get('pager'), client)

        return cls(client=client, **cls_data)
