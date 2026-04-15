from typing import TYPE_CHECKING, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Track
    from yandex_music.music_history.music_history_context_full_model import MusicHistoryContextFullModel
    from yandex_music.music_history.music_history_item_id import MusicHistoryItemId


@model
class MusicHistoryItemData(YandexMusicModel):
    """Класс, представляющий данные элемента истории прослушивания.

    Note:
        Поле `full_model` содержит :obj:`yandex_music.Track` для элементов типа ``track``
        и :obj:`yandex_music.MusicHistoryContextFullModel` для элементов типа ``album``.

    Attributes:
        item_id (:obj:`yandex_music.MusicHistoryItemId`, optional): Идентификатор элемента.
        full_model (:obj:`yandex_music.Track` | :obj:`yandex_music.MusicHistoryContextFullModel`, optional):
            Полная модель элемента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    item_id: Optional['MusicHistoryItemId'] = None
    full_model: Optional[Union['Track', 'MusicHistoryContextFullModel']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.item_id,)

    @classmethod
    def de_json(
        cls,
        data: 'JSONType',
        client: 'ClientType',
        item_type: Optional[str] = None,
    ) -> Optional['MusicHistoryItemData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
            item_type (:obj:`str`, optional): Тип элемента (``track`` или ``album``),
                определяет тип десериализации поля `full_model`.

        Returns:
            :obj:`yandex_music.MusicHistoryItemData`: Данные элемента истории прослушивания.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Track
        from yandex_music.music_history.music_history_context_full_model import MusicHistoryContextFullModel
        from yandex_music.music_history.music_history_item_id import MusicHistoryItemId

        cls_data['item_id'] = MusicHistoryItemId.de_json(cls_data.get('item_id'), client)

        if item_type == 'track':
            cls_data['full_model'] = Track.de_json(cls_data.get('full_model'), client)
        else:
            cls_data['full_model'] = MusicHistoryContextFullModel.de_json(cls_data.get('full_model'), client)

        return cls(client=client, **cls_data)
