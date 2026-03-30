import itertools
from typing import TYPE_CHECKING, List, Optional

from yandex_music import Track, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


@model
class TrackItemId(YandexMusicModel):
    """Класс, представляющий идентификатор трека в истории.

    Attributes:
        track_id (:obj:`str`): Уникальный идентификатор трека.
        album_id (:obj:`str`): Уникальный идентификатор альбома.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track_id: str
    album_id: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track_id, self.album_id)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackItemId']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`TrackItemId`: Идентификатор трека.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        if 'trackId' in data and 'track_id' not in cls_data:
            cls_data['track_id'] = data.get('trackId')
        if 'albumId' in data and 'album_id' not in cls_data:
            cls_data['album_id'] = data.get('albumId')

        return cls(client=client, **cls_data)  # type: ignore


@model
class WaveItemId(YandexMusicModel):
    """Класс, представляющий идентификатор волны в истории.

    Attributes:
        seeds (:obj:`list` из :obj:`str`): Семена волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    seeds: List[str]
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.seeds,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['WaveItemId']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`WaveItemId`: Идентификатор волны.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        return cls(client=client, **cls_data)  # type: ignore


@model
class WaveAgent(YandexMusicModel):
    """Класс, представляющий агента волны.

    Attributes:
        animation_uri (:obj:`str`): URI анимации агента.
        cover (:obj:`dict`, optional): Обложка агента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    animation_uri: str
    cover: Optional[dict] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.animation_uri,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['WaveAgent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`WaveAgent`: Агент волны.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        if 'animationUri' in data and 'animation_uri' not in cls_data:
            cls_data['animation_uri'] = data.get('animationUri')

        return cls(client=client, **cls_data)  # type: ignore


@model
class WaveData(YandexMusicModel):
    """Класс, представляющий данные волны.

    Attributes:
        title (:obj:`str`): Название волны.
        header (:obj:`str`): Заголовок волны.
        station_id (:obj:`str`): Уникальный идентификатор станции.
        seeds (:obj:`list` из :obj:`str`): Семена волны.
        agent (:obj:`WaveAgent`): Агент волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    header: str
    station_id: str
    seeds: List[str]
    agent: 'WaveAgent'
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.header, self.station_id, self.seeds, self.agent)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['WaveData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`WaveData`: Данные волны.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        if 'stationId' in data and 'station_id' not in cls_data:
            cls_data['station_id'] = data.get('stationId')
        if 'agent' in data:
            cls_data['agent'] = WaveAgent.de_json(data.get('agent'), client)  # noqa: F821

        return cls(client=client, **cls_data)  # type: ignore


@model
class WaveFullModel(YandexMusicModel):
    """Класс, представляющий полную модель волны.

    Attributes:
        wave (:obj:`WaveData`): Данные волны.
        simple_wave_foreground_image_url (:obj:`str`, optional): URL изображения переднего плана.
        simple_wave_background_color (:obj:`str`, optional): Цвет фона.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    wave: 'WaveData'
    simple_wave_foreground_image_url: Optional[str] = None
    simple_wave_background_color: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.wave,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['WaveFullModel']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`WaveFullModel`: Полная модель волны.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        wave_data = data.get('wave') or data.get('Wave')
        if wave_data:
            cls_data['wave'] = WaveData.de_json(wave_data, client)  # noqa: F821
        if 'simpleWaveForegroundImageUrl' in data and 'simple_wave_foreground_image_url' not in cls_data:
            cls_data['simple_wave_foreground_image_url'] = data.get('simpleWaveForegroundImageUrl')
        if 'simpleWaveBackgroundColor' in data and 'simple_wave_background_color' not in cls_data:
            cls_data['simple_wave_background_color'] = data.get('simpleWaveBackgroundColor')

        return cls(client=client, **cls_data)  # type: ignore


@model
class TrackContextData(YandexMusicModel):
    """Класс, представляющий данные контекста трека.

    Attributes:
        item_id (:obj:`TrackItemId`): Идентификатор трека.
        full_model (:obj:`yandex_music.Track`): Полная модель трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    item_id: 'TrackItemId'
    full_model: 'Track'
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.item_id, self.full_model)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackContextData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`TrackContextData`: Данные контекста трека.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        item_id_data = data.get('itemId') or data.get('item_id')
        full_model_data = data.get('fullModel') or data.get('full_model')

        cls_data['item_id'] = TrackItemId.de_json(item_id_data, client)  # noqa: F821
        cls_data['full_model'] = Track.de_json(full_model_data, client)

        return cls(client=client, **cls_data)  # type: ignore


@model
class WaveContextData(YandexMusicModel):
    """Класс, представляющий данные контекста волны.

    Attributes:
        item_id (:obj:`WaveItemId`): Идентификатор волны.
        full_model (:obj:`WaveFullModel`): Полная модель волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    item_id: 'WaveItemId'
    full_model: 'WaveFullModel'
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.item_id, self.full_model)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['WaveContextData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`WaveContextData`: Данные контекста волны.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        item_id_data = data.get('itemId') or data.get('item_id')
        full_model_data = data.get('fullModel') or data.get('full_model')

        cls_data['item_id'] = WaveItemId.de_json(item_id_data, client)  # noqa: F821
        cls_data['full_model'] = WaveFullModel.de_json(full_model_data, client)  # noqa: F821

        return cls(client=client, **cls_data)  # type: ignore


@model
class HistoryTabContext(YandexMusicModel):
    """Класс, представляющий контекст вкладки истории.

    Note:
        Известные значения поля `type`: `search`, `wave`.

        В зависимости от типа поля `type`, поле `data` может быть заполнено или отсутствовать.

    Attributes:
        type (:obj:`str`): Тип контекста.
        data (:obj:`WaveContextData`, optional): Данные контекста (для типа `wave`).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    data: Optional['WaveContextData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['HistoryTabContext']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`HistoryTabContext`: Контекст вкладки истории.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        context_type = data.get('type')
        if context_type == 'wave':
            cls_data['data'] = WaveContextData.de_json(data.get('data'), client)  # noqa: F821

        return cls(client=client, **cls_data)  # type: ignore


@model
class HistoryTrack(YandexMusicModel):
    """Класс, представляющий трек в истории.

    Note:
        Известные значения поля `type`: `track`.

    Attributes:
        type (:obj:`str`): Тип элемента.
        data (:obj:`TrackContextData`): Данные трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    data: 'TrackContextData'
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['HistoryTrack']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`HistoryTrack`: Трек в истории.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        cls_data['data'] = TrackContextData.de_json(data.get('data'), client)  # noqa: F821

        return cls(client=client, **cls_data)  # type: ignore


@model
class HistoryTabItem(YandexMusicModel):
    """Класс, представляющий элемент вкладки истории.

    Attributes:
        context (:obj:`HistoryTabContext`): Контекст элемента.
        tracks (:obj:`list` из :obj:`HistoryTrack`): Треки в истории.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    context: 'HistoryTabContext'
    tracks: List['HistoryTrack']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.context, self.tracks)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['HistoryTabItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`HistoryTabItem`: Элемент вкладки истории.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        cls_data['context'] = HistoryTabContext.de_json(data.get('context'), client)  # noqa: F821
        cls_data['tracks'] = HistoryTrack.de_list(data.get('tracks'), client)  # noqa: F821

        return cls(client=client, **cls_data)  # type: ignore


@model
class HistoryTab(YandexMusicModel):
    """Класс, представляющий вкладку истории прослушивания.

    Attributes:
        date (:obj:`str`): Дата в формате YYYY-MM-DD.
        items (:obj:`list` из :obj:`HistoryTabItem`): Элементы вкладки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    date: str
    items: List['HistoryTabItem']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.date, self.items)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['HistoryTab']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`HistoryTab`: Вкладка истории.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        cls_data['items'] = HistoryTabItem.de_list(data.get('items'), client)  # noqa: F821

        return cls(client=client, **cls_data)  # type: ignore

    @staticmethod
    def extract_tracks(history_tabs: List['HistoryTab']) -> List['Track']:
        """Извлечение всех треков из списка вкладок истории.

        Args:
            history_tabs (:obj:`list` из :obj:`HistoryTab`): Список вкладок истории.

        Returns:
            :obj:`list` из :obj:`yandex_music.Track`: Список треков.
        """

        def get_track_from_history_track(history_track: 'HistoryTrack') -> 'Track':
            return history_track.data.full_model

        def get_tracks_from_item(item: 'HistoryTabItem') -> List['Track']:
            return list(
                map(
                    get_track_from_history_track,
                    filter(lambda ht: isinstance(ht, HistoryTrack) and ht.data, item.tracks),
                )
            )

        def get_tracks_from_tab(tab: 'HistoryTab') -> List['Track']:
            return list(itertools.chain.from_iterable(map(get_tracks_from_item, tab.items)))

        return list(itertools.chain.from_iterable(map(get_tracks_from_tab, history_tabs)))
