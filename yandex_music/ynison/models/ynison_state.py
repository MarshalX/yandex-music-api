"""Модели Ynison State."""

from dataclasses import dataclass
from typing import List, Optional

import betterproto


class DeviceType(betterproto.Enum):
    """Тип устройства.

    Attributes:
        UNSPECIFIED: Не указан.
        WEB: Браузер.
        ANDROID: Android-телефон/планшет.
        IOS: iOS-телефон/планшет.
        SMART_SPEAKER: Умная колонка.
        WEB_TV: Web-телевизор.
        ANDROID_TV: Android-телевизор.
        APPLE_TV: Apple-телевизор.
        ANDROID_WEAR: Android-часы.
        WEB_DESKTOP: Desktop-приложение веба для Windows.
    """

    UNSPECIFIED = 0
    WEB = 1
    ANDROID = 2
    IOS = 3
    SMART_SPEAKER = 4
    WEB_TV = 5
    ANDROID_TV = 6
    APPLE_TV = 7
    ANDROID_WEAR = 8
    WEB_DESKTOP = 9


class PlayablePlayableType(betterproto.Enum):
    """Тип проигрываемой сущности.

    Attributes:
        UNSPECIFIED: Не указан.
        TRACK: Обычный трек.
        LOCAL_TRACK: Локальный трек с устройства.
        INFINITE: Бесконечный поток (радио/нейромузыка).
        VIDEO_CLIP: Видеоклип.
    """

    UNSPECIFIED = 0
    TRACK = 1
    LOCAL_TRACK = 2
    INFINITE = 3
    VIDEO_CLIP = 4


class VideoClipInfoRecommendationType(betterproto.Enum):
    """Способ попадания видеоклипа в очередь.

    Attributes:
        UNSPECIFIED: Не указан.
        RECOMMENDED: Видеоклип пришёл из рекомендаций.
        ON_DEMAND: Видеоклип явно выбран пользователем.
        SEARCH: Видеоклип выбран из поиска.
        ARTIST: Видеоклип выбран с экрана артиста.
        OWN: Видеоклип выбран в собственной коллекции.
        EDITORIAL_CHOICE: Видеоклип пришёл в блоке рекомендаций на странице трендов.
    """

    UNSPECIFIED = 0
    RECOMMENDED = 1
    ON_DEMAND = 2
    SEARCH = 3
    ARTIST = 4
    OWN = 5
    EDITORIAL_CHOICE = 6


class PlayerQueueEntityType(betterproto.Enum):
    """Тип сущности, от которой порождена очередь (устаревший, см. :class:`PlayerQueueQueue`).

    Attributes:
        UNSPECIFIED: Не указан.
        ARTIST: Очередь популярных треков артиста.
        PLAYLIST: Очередь треков из плейлиста.
        ALBUM: Очередь треков альбома.
        RADIO: Динамическая очередь радио по seed'у станции.
        VARIOUS: Случайный набор треков.
        GENERATIVE: Поток нейромузыки.
        FM_RADIO: Поток FM-радио.
        VIDEO_WAVE: Динамическая очередь видеоклипов.
        LOCAL_TRACKS: Очередь локальных треков с устройства.
    """

    UNSPECIFIED = 0
    ARTIST = 1
    PLAYLIST = 2
    ALBUM = 3
    RADIO = 4
    VARIOUS = 5
    GENERATIVE = 6
    FM_RADIO = 7
    VIDEO_WAVE = 8
    LOCAL_TRACKS = 9


class PlayerQueueEntityContext(betterproto.Enum):
    """Контекст воспроизведения очереди.

    Attributes:
        BASED_ON_ENTITY_BY_DEFAULT: Контекст выбран по умолчанию в зависимости от сущности.
        USER_TRACKS: Мои треки.
        DOWNLOADED_TRACKS: Скачанные треки.
        SEARCH: Из поиска.
        MUSIC_HISTORY: История прослушивания.
        MUSIC_HISTORY_SEARCH: Поиск по истории прослушивания.
        ARTIST_MY_COLLECTION: Коллекция артиста у пользователя.
        ARTIST_FAMILIAR_FROM_WAVE: Артисты, знакомые по волне.
    """

    BASED_ON_ENTITY_BY_DEFAULT = 0
    USER_TRACKS = 1
    DOWNLOADED_TRACKS = 2
    SEARCH = 3
    MUSIC_HISTORY = 4
    MUSIC_HISTORY_SEARCH = 5
    ARTIST_MY_COLLECTION = 6
    ARTIST_FAMILIAR_FROM_WAVE = 7


class PlayerQueueQueueWaveQueueEntityOptionsWaveSourceSourceType(betterproto.Enum):
    """Способ попадания трека в волновую очередь.

    Attributes:
        ONLINE_BY_DEFAULT: Трек пришёл из онлайн-рекомендаций.
        OFFLINE: Трек пришёл из оффлайн-рекомендаций (оффлайн-волна).
    """

    ONLINE_BY_DEFAULT = 0
    OFFLINE = 1


class PlayerStateOptionsRepeatMode(betterproto.Enum):
    """Режим повтора воспроизведения.

    Attributes:
        UNSPECIFIED: Не указан.
        NONE: Без повтора.
        ONE: Повтор текущего трека.
        ALL: Повтор всей очереди.
    """

    UNSPECIFIED = 0
    NONE = 1
    ONE = 2
    ALL = 3


class PlayerQueueInjectPlayablePlayableType(betterproto.Enum):
    """Тип инжектируемой в очередь сущности.

    Attributes:
        UNSPECIFIED: Не указан.
        ALICE_SHOT: Голосовая врезка Алисы.
        AD: Рекламный блок.
        PREROLL: Преролл.
    """

    UNSPECIFIED = 0
    ALICE_SHOT = 1
    AD = 2
    PREROLL = 3


class PutYnisonStateRequestActivityInterceptionType(betterproto.Enum):
    """Тактика перехвата активности устройством, отправившим сообщение.

    Attributes:
        DO_NOT_INTERCEPT_BY_DEFAULT: Устройство не пытается перехватить активность.
        INTERCEPT_IF_NO_ONE_ACTIVE: Устройство становится активным, если на момент обработки
            активное устройство отсутствует.
        INTERCEPT_EAGER: Устройство получает активность после успешной обработки сообщения.
    """

    DO_NOT_INTERCEPT_BY_DEFAULT = 0
    INTERCEPT_IF_NO_ONE_ACTIVE = 1
    INTERCEPT_EAGER = 2


@dataclass
class Playable(betterproto.Message):
    """Класс, представляющий проигрываемую сущность.

    Может быть треком, видеоклипом и т.п.

    Attributes:
        playable_id (:obj:`str`): Идентификатор сущности.
        album_id_optional (:obj:`str`, optional): Опциональный идентификатор альбома.
            Используется для составного идентификатора playable при ``playable_type == TRACK``.
        playable_type (:obj:`yandex_music.ynison.models.ynison_state.PlayablePlayableType`):
            Тип сущности.
        from_ (:obj:`str`): Фром для play-audio.
        title (:obj:`str`): Заголовок.
        cover_url_optional (:obj:`str`, optional): Опциональная ссылка на обложку.
            Может содержать плейсхолдер для размера в аватарнице.
        video_clip_info (:obj:`yandex_music.ynison.models.ynison_state.VideoClipInfo`):
            Дополнительная информация о видеоклипе (в oneof с ``track_info``).
        track_info (:obj:`yandex_music.ynison.models.ynison_state.TrackInfo`):
            Дополнительная информация о треке (в oneof с ``video_clip_info``).
        navigation_id_optional (:obj:`str`, optional): Хеш для play-audio. Используется для
            определения хеша навигации пользователя при изменении проигрываемой сущности в очереди.
        playback_action_id_optional (:obj:`str`, optional): Уникальный идентификатор действия
            воспроизведения. Используется для аналитики, чтобы склеить воспроизведение playable
            с экраном, с которого было сгенерировано поле.
    """

    playable_id: str = betterproto.string_field(1)
    album_id_optional: Optional[str] = betterproto.message_field(2, wraps=betterproto.TYPE_STRING)
    playable_type: 'PlayablePlayableType' = betterproto.enum_field(3)
    from_: str = betterproto.string_field(4)
    title: str = betterproto.string_field(5)
    cover_url_optional: Optional[str] = betterproto.message_field(6, wraps=betterproto.TYPE_STRING)
    video_clip_info: 'VideoClipInfo' = betterproto.message_field(7, group='additional_info_optional')
    track_info: 'TrackInfo' = betterproto.message_field(8, group='additional_info_optional')
    navigation_id_optional: Optional[str] = betterproto.message_field(9, wraps=betterproto.TYPE_STRING)
    playback_action_id_optional: Optional[str] = betterproto.message_field(10, wraps=betterproto.TYPE_STRING)


@dataclass
class VideoClipInfo(betterproto.Message):
    """Класс, представляющий дополнительную информацию о видеоклипе.

    Attributes:
        recommendation_type (:obj:`yandex_music.ynison.models.ynison_state.VideoClipInfoRecommendationType`):
            Способ попадания видеоклипа в очередь (для аналитики).
    """

    recommendation_type: 'VideoClipInfoRecommendationType' = betterproto.enum_field(1)


@dataclass
class TrackInfo(betterproto.Message):
    """Класс, представляющий дополнительную информацию о треке.

    Attributes:
        track_source_key (:obj:`int`): Ключ источника из
            ``[WaveQueue.EntityOptions.track_sources]``.
        batch_id_optional (:obj:`str`, optional): Идентификатор батча рекомендаций.
            Требуется для треков из волновой очереди; для прослушанных треков
            можно не переносить.
    """

    track_source_key: int = betterproto.uint32_field(1)
    batch_id_optional: Optional[str] = betterproto.message_field(2, wraps=betterproto.TYPE_STRING)


@dataclass
class UpdateVersion(betterproto.Message):
    """Класс, представляющий версию изменений.

    Attributes:
        device_id (:obj:`str`): Идентификатор устройства, которое инициировало изменение.
        version (:obj:`int`): Версия последнего изменения. Случайное значение int64.
        timestamp_ms (:obj:`int`): Время последнего изменения, диагностическое значение,
            не используется в бизнес-логике на клиентах.
    """

    device_id: str = betterproto.string_field(1)
    version: int = betterproto.int64_field(2)
    timestamp_ms: int = betterproto.int64_field(3)


@dataclass
class PlayerQueue(betterproto.Message):
    """Класс, представляющий очередь воспроизведения.

    Attributes:
        entity_id (:obj:`str`): Идентификатор сущности (альбома/плейлиста/радио и др.).
            Устаревшее поле; новый клиент должен читать и писать ``queue``.
        entity_type (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueEntityType`):
            Тип сущности. Устаревшее поле; новый клиент должен использовать ``queue``.
        queue (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueue`):
            Новая иерархическая структура очередей с oneof по типам.
        current_playable_index (:obj:`int`): Индекс текущего playable в списке ``playable_list``.
        playable_list (:obj:`list` из :obj:`yandex_music.ynison.models.ynison_state.Playable`):
            Список сущностей в очереди.
        options (:obj:`yandex_music.ynison.models.ynison_state.PlayerStateOptions`):
            Настройки плеера.
        version (:obj:`yandex_music.ynison.models.ynison_state.UpdateVersion`):
            Версия последнего изменения очереди.
        shuffle_optional (:obj:`yandex_music.ynison.models.ynison_state.Shuffle`):
            Настройки шаффла. При выключенном шаффле не приходят.
        entity_context (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueEntityContext`):
            Контекст воспроизведения. Устаревшее поле; контекст теперь применяется только
            к сущностям из фонотеки в ``queue``.
        from_optional (:obj:`str`, optional): Опциональный фром очереди. Используется,
            когда фром нельзя достать из ``playable_list`` (например, пустая ЕОВ-очередь радио).
        initial_entity_optional (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueInitialEntity`):
            Изначальный id+type сущности, которой была проинициализирована очередь. Устаревшее
            поле; источник трека теперь берётся из ``[WaveQueue.EntityOptions.track_sources]``.
        adding_options_optional (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueuePlayerQueueOptions`):
            Дополнительные параметры. Устаревшее поле; см. ``queue``.
        navigation_id_optional (:obj:`str`, optional): Поле обратной совместимости для клиентов
            без поддержки WaveQueue. Работает как ``[WaveQueue.navigation_id_optional]``.
        filter_optional (:obj:`str`, optional): Поле обратной совместимости для клиентов
            без поддержки WaveQueue. Работает как ``[WaveQueue.EntityOptions.PlaylistId.filter_optional]``.
        playback_action_id_optional (:obj:`str`, optional): Поле обратной совместимости для клиентов
            без поддержки WaveQueue. Работает как ``[WaveQueue.playback_action_id_optional]``.
    """

    entity_id: str = betterproto.string_field(1)
    entity_type: 'PlayerQueueEntityType' = betterproto.enum_field(2)
    queue: 'PlayerQueueQueue' = betterproto.message_field(12)
    current_playable_index: int = betterproto.int32_field(3)
    playable_list: List['Playable'] = betterproto.message_field(4)
    options: 'PlayerStateOptions' = betterproto.message_field(5)
    version: 'UpdateVersion' = betterproto.message_field(6)
    shuffle_optional: 'Shuffle' = betterproto.message_field(7)
    entity_context: 'PlayerQueueEntityContext' = betterproto.enum_field(8)
    from_optional: Optional[str] = betterproto.message_field(9, wraps=betterproto.TYPE_STRING)
    initial_entity_optional: 'PlayerQueueInitialEntity' = betterproto.message_field(10)
    adding_options_optional: 'PlayerQueuePlayerQueueOptions' = betterproto.message_field(11)
    navigation_id_optional: Optional[str] = betterproto.message_field(13, wraps=betterproto.TYPE_STRING)
    filter_optional: Optional[str] = betterproto.message_field(14, wraps=betterproto.TYPE_STRING)
    playback_action_id_optional: Optional[str] = betterproto.message_field(15, wraps=betterproto.TYPE_STRING)


@dataclass
class PlayerQueueQueue(betterproto.Message):
    """Класс, представляющий иерархическую структуру очередей.

    Каждому виду очередей соответствует один из типов :class:`PlayablePlayableType`.
    Каждому playable'у с типом ``TRACK`` соответствует сущность из таблицы сущностей
    (см. :class:`PlayerQueueQueueWaveQueueEntityOptions`). Очереди не имеют универсального
    идентификатора — каждая сама решает, что её идентифицирует (см. :attr:`type`).

    Attributes:
        wave_queue (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueue`):
            Волновая очередь (в oneof ``type``).
        generative_queue (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueGenerativeQueue`):
            Очередь нейромузыки (в oneof ``type``).
        fm_radio_queue (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueFmRadioQueue`):
            Очередь FM-радио (в oneof ``type``).
        video_wave_queue (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueVideoWaveQueue`):
            Очередь видеоклипов (в oneof ``type``).
        local_tracks_queue (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueLocalTracksQueue`):
            Очередь локальных треков с устройства (в oneof ``type``).
    """

    wave_queue: 'PlayerQueueQueueWaveQueue' = betterproto.message_field(1, group='type')
    generative_queue: 'PlayerQueueQueueGenerativeQueue' = betterproto.message_field(2, group='type')
    fm_radio_queue: 'PlayerQueueQueueFmRadioQueue' = betterproto.message_field(3, group='type')
    video_wave_queue: 'PlayerQueueQueueVideoWaveQueue' = betterproto.message_field(4, group='type')
    local_tracks_queue: 'PlayerQueueQueueLocalTracksQueue' = betterproto.message_field(5, group='type')


@dataclass
class PlayerQueueQueueWaveQueue(betterproto.Message):
    """Класс, представляющий волновую очередь.

    Состоит из :attr:`PlayablePlayableType.TRACK`. Автоматически продлевается, если треки
    закончились. Поддерживает «Скип», «Лайк/Дизлайк», «Играть следующим», «Добавить в очередь»,
    «Удалить», «Переместить», «Повтор трека».

    Может находиться в двух состояниях:

    1. Играли только треки фонотечных сущностей, но ещё не были запрошены рекомендательные треки.
       В этом состоянии :attr:`entity_options.wave_entity_optional` не задано.
    2. Рекомендательные треки были запрошены. В таблице сущностей появляется единственная
       уникальная запись :class:`PlayerQueueQueueWaveQueueEntityOptionsWaveSession`, которую
       можно использовать как идентификатор очереди.

    Очередь состоит из трёх частей: прослушанные треки (в ``playable_list``), добавленные
    в очередь непрослушанные треки (в ``playable_list``), непрослушанные рекомендованные
    треки (в ``recommended_playable_list``).

    Attributes:
        recommended_playable_list (:obj:`list` из :obj:`yandex_music.ynison.models.ynison_state.Playable`):
            Непрослушанные рекомендованные треки. У таких треков следует передавать ``batch_id``.
            Список может быть непустым только если заполнено ``entity_options.wave_entity_optional``.
            Исторический нюанс: в ``playable_list`` в конце при наличии лежит один первый
            рекомендованный трек для отображения обложки следующего трека в плеере.
        live_playable_index (:obj:`int`): Индекс последнего прослушанного трека в состоянии
            «с рекомендательными треками»; индекс потенциального рекомендательного трека
            в состоянии «без рекомендательных треков». Возможны значения ``[current_playable_index,
            playable_list.size)`` в первом состоянии и ``playable_list.size`` во втором.
            Значение ``-1`` — пустая очередь.
        entity_options (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptions`):
            Параметры сущностей для смешанной трековой очереди.
        navigation_id_optional (:obj:`str`, optional): Хеш очереди для аналитики новых фромов,
            чтобы склеить воспроизведения с полной навигацией пользователя. Генерируется один
            раз для очереди и восстанавливается при синхронизации с клиентами.
        playback_action_id_optional (:obj:`str`, optional): Идентификатор действия воспроизведения,
            сгенерированный клиентом при запуске очереди. Используется для аналитики, чтобы
            склеить воспроизведение playable с экраном, с которого было сгенерировано поле.
    """

    recommended_playable_list: List['Playable'] = betterproto.message_field(1)
    live_playable_index: int = betterproto.int32_field(2)
    entity_options: 'PlayerQueueQueueWaveQueueEntityOptions' = betterproto.message_field(3)
    navigation_id_optional: Optional[str] = betterproto.message_field(4, wraps=betterproto.TYPE_STRING)
    playback_action_id_optional: Optional[str] = betterproto.message_field(5, wraps=betterproto.TYPE_STRING)


@dataclass
class PlayerQueueQueueWaveQueueEntityOptions(betterproto.Message):
    """Класс, представляющий параметры сущностей волновой очереди.

    Attributes:
        wave_entity_optional (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptionsWaveSession`):
            Идентификатор rotor-сессии, к которой относятся все рекомендованные треки
            в этой очереди. Если поле задано, очередь бесконечно достраивается из этой
            сессии; иначе достраиваться не может.
        track_sources (:obj:`list` из :obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptionsTrackSourceWithKey`):
            Таблица контекстов/сущностей очереди для оптимизации объёма стейта.
    """

    wave_entity_optional: 'PlayerQueueQueueWaveQueueEntityOptionsWaveSession' = betterproto.message_field(1)
    track_sources: List['PlayerQueueQueueWaveQueueEntityOptionsTrackSourceWithKey'] = betterproto.message_field(2)


@dataclass
class PlayerQueueQueueWaveQueueEntityOptionsWaveSession(betterproto.Message):
    """Класс, представляющий rotor-сессию волновой очереди.

    Attributes:
        session_id (:obj:`str`): Идентификатор rotor-сессии.
    """

    session_id: str = betterproto.string_field(1)


@dataclass
class PlayerQueueQueueWaveQueueEntityOptionsTrackSourceWithKey(betterproto.Message):
    """Класс, представляющий запись в таблице источников треков с ключом.

    Attributes:
        key (:obj:`int`): Ключ для доступа к сущности. Должен быть уникальным в рамках таблицы;
            стабильность не требуется, но в рамках одного стейта должен быть консистентным.
        wave_source (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptionsWaveSource`):
            Волновой источник (в oneof ``track_source``).
        phonoteka_source (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptionsPhonotekaSource`):
            Фонотечный источник (в oneof ``track_source``).
    """

    key: int = betterproto.uint32_field(1)
    wave_source: 'PlayerQueueQueueWaveQueueEntityOptionsWaveSource' = betterproto.message_field(2, group='track_source')
    phonoteka_source: 'PlayerQueueQueueWaveQueueEntityOptionsPhonotekaSource' = betterproto.message_field(
        3, group='track_source'
    )


@dataclass
class PlayerQueueQueueWaveQueueEntityOptionsWaveSource(betterproto.Message):
    """Класс, представляющий волновой источник попадания трека в очередь.

    Трек в волну попадает в результате ответа рекомендаций. Рекомендации делятся на
    онлайн- и оффлайн-рекомендации (оффлайн-волна).

    Attributes:
        source_type (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptionsWaveSourceSourceType`):
            Способ попадания трека в волновую очередь.
    """

    source_type: 'PlayerQueueQueueWaveQueueEntityOptionsWaveSourceSourceType' = betterproto.enum_field(1)


@dataclass
class PlayerQueueQueueWaveQueueEntityOptionsPhonotekaSource(betterproto.Message):
    """Класс, представляющий фонотечный источник попадания трека в очередь.

    Attributes:
        artist_id (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptionsArtistId`):
            Идентификатор артиста (в oneof ``id``).
        playlist_id (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptionsPlaylistId`):
            Идентификатор плейлиста (в oneof ``id``).
        album_id (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueQueueWaveQueueEntityOptionsAlbumId`):
            Идентификатор альбома (в oneof ``id``).
        entity_context (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueEntityContext`):
            Контекст воспроизведения.
    """

    artist_id: 'PlayerQueueQueueWaveQueueEntityOptionsArtistId' = betterproto.message_field(2, group='id')
    playlist_id: 'PlayerQueueQueueWaveQueueEntityOptionsPlaylistId' = betterproto.message_field(3, group='id')
    album_id: 'PlayerQueueQueueWaveQueueEntityOptionsAlbumId' = betterproto.message_field(4, group='id')
    entity_context: 'PlayerQueueEntityContext' = betterproto.enum_field(1)


@dataclass
class PlayerQueueQueueWaveQueueEntityOptionsArtistId(betterproto.Message):
    """Класс, представляющий идентификатор артиста в фонотечном источнике.

    Attributes:
        id (:obj:`str`): Идентификатор артиста. Строковый по историческим причинам.
    """

    id: str = betterproto.string_field(1)


@dataclass
class PlayerQueueQueueWaveQueueEntityOptionsPlaylistId(betterproto.Message):
    """Класс, представляющий идентификатор плейлиста в фонотечном источнике.

    Attributes:
        id (:obj:`str`): Идентификатор плейлиста. Строковый из-за процесса отказа от ``owner:kind``.
        filter_optional (:obj:`str`, optional): Идентификатор фильтра для плейлиста.
            Если запущены все треки плейлиста — :obj:`None`; иначе — ``filter_id``, откуда
            были запущены треки.
    """

    id: str = betterproto.string_field(1)
    filter_optional: Optional[str] = betterproto.message_field(2, wraps=betterproto.TYPE_STRING)


@dataclass
class PlayerQueueQueueWaveQueueEntityOptionsAlbumId(betterproto.Message):
    """Класс, представляющий идентификатор альбома в фонотечном источнике.

    Attributes:
        id (:obj:`str`): Идентификатор альбома. Строковый по историческим причинам.
    """

    id: str = betterproto.string_field(1)


@dataclass
class PlayerQueueQueueGenerativeQueue(betterproto.Message):
    """Класс, представляющий поток нейромузыки.

    Состоит из одного :attr:`PlayablePlayableType.INFINITE`.

    Attributes:
        id (:obj:`str`): Идентификатор потока.
    """

    id: str = betterproto.string_field(1)


@dataclass
class PlayerQueueQueueFmRadioQueue(betterproto.Message):
    """Класс, представляющий поток FM-радио.

    Состоит из одного :attr:`PlayablePlayableType.INFINITE`.

    Attributes:
        id (:obj:`str`): Идентификатор потока.
    """

    id: str = betterproto.string_field(1)


@dataclass
class PlayerQueueQueueVideoWaveQueue(betterproto.Message):
    """Класс, представляющий рекомендательную очередь видеоклипов.

    Состоит из :attr:`PlayablePlayableType.VIDEO_CLIP`.

    Attributes:
        id (:obj:`str`): Идентификатор очереди. Произвольная строка: например, ``default``,
            ``other``, ``search:${clipId}``, ``${albumId}``.
    """

    id: str = betterproto.string_field(1)


@dataclass
class PlayerQueueQueueLocalTracksQueue(betterproto.Message):
    """Класс, представляющий очередь локальных треков с устройства.

    Состоит из :attr:`PlayablePlayableType.LOCAL_TRACK`. Такую очередь нельзя перенести через
    Ynison на другое устройство, но можно отобразить простейший пульт. Локальные треки не могут
    быть перемешаны с обычными треками (:attr:`PlayablePlayableType.TRACK`).
    """


@dataclass
class PlayerQueueInitialEntity(betterproto.Message):
    """Класс, представляющий изначальную сущность очереди (устаревший).

    Attributes:
        entity_id (:obj:`str`): Идентификатор сущности.
        entity_type (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueEntityType`):
            Тип сущности.
    """

    entity_id: str = betterproto.string_field(1)
    entity_type: 'PlayerQueueEntityType' = betterproto.enum_field(2)


@dataclass
class PlayerQueuePlayerQueueOptions(betterproto.Message):
    """Класс, представляющий дополнительные параметры очереди (устаревший).

    Attributes:
        radio_options (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueuePlayerQueueOptionsRadioOptions`):
            Параметры радио-очереди (в oneof ``options``).
    """

    radio_options: 'PlayerQueuePlayerQueueOptionsRadioOptions' = betterproto.message_field(1, group='options')


@dataclass
class PlayerQueuePlayerQueueOptionsRadioOptions(betterproto.Message):
    """Класс, представляющий параметры радио-очереди (устаревший).

    Для ``entity_type == RADIO(4)``. Информация о волновой очереди теперь находится
    в ``[WaveQueue.EntityOptions.wave_entity_optional]``.

    Attributes:
        session_id (:obj:`str`): Идентификатор rotor-сессии.
    """

    session_id: str = betterproto.string_field(1)


@dataclass
class PlayerStateOptions(betterproto.Message):
    """Класс, представляющий настройки плеера.

    Attributes:
        repeat_mode (:obj:`yandex_music.ynison.models.ynison_state.PlayerStateOptionsRepeatMode`):
            Режим повтора.
    """

    repeat_mode: 'PlayerStateOptionsRepeatMode' = betterproto.enum_field(1)


@dataclass
class Shuffle(betterproto.Message):
    """Класс, представляющий настройки шаффла.

    Attributes:
        playable_indices (:obj:`list` из :obj:`int`): Перемешанный список индексов сущностей
            в очереди.
    """

    playable_indices: List[int] = betterproto.uint32_field(1)


@dataclass
class Device(betterproto.Message):
    """Класс, представляющий устройство.

    Attributes:
        info (:obj:`yandex_music.ynison.models.ynison_state.DeviceInfo`):
            Информация об устройстве.
        volume (:obj:`float`): Громкость. Устаревшее значение, см. ``volume_info``.
        capabilities (:obj:`yandex_music.ynison.models.ynison_state.DeviceCapabilities`):
            Настройки доступности.
        session (:obj:`yandex_music.ynison.models.ynison_state.Session`):
            Информация о сессии; уникальна для каждого отдельно инициализированного подключения.
        is_offline (:obj:`bool`): Оффлайн ли устройство (не подключено к Ynison на данный момент).
        volume_info (:obj:`yandex_music.ynison.models.ynison_state.DeviceVolume`):
            Состояние громкости устройства вместе с информацией о последнем изменившем её
            устройстве.
    """

    info: 'DeviceInfo' = betterproto.message_field(1)
    volume: float = betterproto.double_field(2)
    capabilities: 'DeviceCapabilities' = betterproto.message_field(3)
    session: 'Session' = betterproto.message_field(4)
    is_offline: bool = betterproto.bool_field(5)
    volume_info: 'DeviceVolume' = betterproto.message_field(6)


@dataclass
class DeviceVolume(betterproto.Message):
    """Класс, представляющий состояние громкости устройства.

    Attributes:
        volume (:obj:`float`): Громкость в интервале ``[0.0; 1.0]``. Значение тесно связано
            с ``[DeviceCapabilities.volume_granularity]``; ожидается округление мантиссы
            до 4 знаков при делении ``1.0`` на число шагов шкалы.
        version (:obj:`yandex_music.ynison.models.ynison_state.UpdateVersion`):
            Версия последнего изменения громкости устройства.
    """

    volume: float = betterproto.double_field(1)
    version: 'UpdateVersion' = betterproto.message_field(2)


@dataclass
class DeviceInfo(betterproto.Message):
    """Класс, представляющий информацию об устройстве.

    Attributes:
        device_id (:obj:`str`): Идентификатор устройства.
        title (:obj:`str`): Название устройства.
        type (:obj:`yandex_music.ynison.models.ynison_state.DeviceType`): Тип устройства.
        app_name (:obj:`str`): Информация о клиентском приложении подключённого устройства.
        app_version (:obj:`str`): Информация о версии клиентского приложения.
    """

    device_id: str = betterproto.string_field(1)
    title: str = betterproto.string_field(2)
    type: 'DeviceType' = betterproto.enum_field(3)
    app_name: str = betterproto.string_field(4)
    app_version: str = betterproto.string_field(5)


@dataclass
class DeviceCapabilities(betterproto.Message):
    """Класс, представляющий настройки доступности устройства.

    Attributes:
        can_be_player (:obj:`bool`): Может ли устройство быть активным и проигрывать сущности.
        can_be_remote_controller (:obj:`bool`): Может ли устройство быть пультом.
        volume_granularity (:obj:`int`): Максимальное количество делений на шкале громкости
            для управления этим устройством. ``0`` — устройство не поддерживает удалённый
            контроль громкости; ``N`` — поддерживает. Допустимы значения ``[0, 1000]``.
    """

    can_be_player: bool = betterproto.bool_field(1)
    can_be_remote_controller: bool = betterproto.bool_field(2)
    volume_granularity: int = betterproto.uint32_field(3)


@dataclass
class Session(betterproto.Message):
    """Класс, представляющий сессию подключения устройства.

    Attributes:
        id (:obj:`int`): Идентификатор сессии. Сервер сгенерирует случайное значение
            самостоятельно; клиент может заполнить это значение при ``UpdateFullState``,
            и тогда сервер использует переданное.
    """

    id: int = betterproto.int64_field(1)


@dataclass
class PlayingStatus(betterproto.Message):
    """Класс, представляющий статус воспроизведения.

    Attributes:
        progress_ms (:obj:`int`): Прогресс проигрываемой сущности в миллисекундах,
            в интервале ``[0; длина]``. Для infinite-очередей равен ``0``.
        duration_ms (:obj:`int`): Длительность проигрываемой сущности в миллисекундах.
            Для infinite-очередей равна ``0``.
        paused (:obj:`bool`): Был ли трек поставлен на паузу.
        playback_speed (:obj:`float`): Скорость воспроизведения.
        version (:obj:`yandex_music.ynison.models.ynison_state.UpdateVersion`):
            Версия последнего изменения статуса воспроизведения.
    """

    progress_ms: int = betterproto.int64_field(1)
    duration_ms: int = betterproto.int64_field(2)
    paused: bool = betterproto.bool_field(3)
    playback_speed: float = betterproto.double_field(4)
    version: 'UpdateVersion' = betterproto.message_field(5)


@dataclass
class PlayerQueueInject(betterproto.Message):
    """Класс, представляющий состояние проигрывания инжектируемой в очередь сущности.

    Инжектироваться может шот, преролл и т.п.

    Attributes:
        playing_status (:obj:`yandex_music.ynison.models.ynison_state.PlayingStatus`):
            Статус воспроизведения.
        playable (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueInjectPlayable`):
            Дополнительная проигрываемая сущность.
        version (:obj:`yandex_music.ynison.models.ynison_state.UpdateVersion`):
            Версия последнего изменения состояния.
    """

    playing_status: 'PlayingStatus' = betterproto.message_field(1)
    playable: 'PlayerQueueInjectPlayable' = betterproto.message_field(2)
    version: 'UpdateVersion' = betterproto.message_field(3)


@dataclass
class PlayerQueueInjectPlayable(betterproto.Message):
    """Класс, представляющий инжектируемую в очередь сущность.

    Attributes:
        playable_id (:obj:`str`): Идентификатор сущности.
        playable_type (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueInjectPlayablePlayableType`):
            Тип сущности.
        title (:obj:`str`): Заголовок.
        cover_url (:obj:`str`, optional): Опциональная ссылка на обложку. Может содержать
            плейсхолдер для размера в аватарнице.
    """

    playable_id: str = betterproto.string_field(1)
    playable_type: 'PlayerQueueInjectPlayablePlayableType' = betterproto.enum_field(2)
    title: str = betterproto.string_field(3)
    cover_url: Optional[str] = betterproto.message_field(4, wraps=betterproto.TYPE_STRING)


@dataclass
class PlayerState(betterproto.Message):
    """Класс, представляющий состояние плеера.

    Attributes:
        status (:obj:`yandex_music.ynison.models.ynison_state.PlayingStatus`):
            Статус воспроизведения.
        player_queue (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueue`):
            Текущая очередь.
        player_queue_inject_optional (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueInject`):
            Состояние проигрывания инжектируемой в очередь сущности.
    """

    status: 'PlayingStatus' = betterproto.message_field(1)
    player_queue: 'PlayerQueue' = betterproto.message_field(2)
    player_queue_inject_optional: 'PlayerQueueInject' = betterproto.message_field(3)


@dataclass
class PutYnisonStateRequest(betterproto.Message):
    """Класс, представляющий запрос на обновление состояния Ynison.

    Клиент отправляет на сервер один из параметров в зависимости от произошедшего события.

    Attributes:
        update_full_state (:obj:`yandex_music.ynison.models.ynison_state.UpdateFullState`):
            Обновить общее состояние (в oneof ``parameters``).
        update_active_device (:obj:`yandex_music.ynison.models.ynison_state.UpdateActiveDevice`):
            Обновить активное устройство (в oneof ``parameters``).
        update_playing_status (:obj:`yandex_music.ynison.models.ynison_state.UpdatePlayingStatus`):
            Обновить статус воспроизведения (в oneof ``parameters``).
        update_player_state (:obj:`yandex_music.ynison.models.ynison_state.UpdatePlayerState`):
            Обновить состояние плеера (в oneof ``parameters``).
        update_volume (:obj:`yandex_music.ynison.models.ynison_state.UpdateVolume`):
            Обновить громкость (устаревшее, см. :attr:`update_volume_info`).
        update_player_queue_inject (:obj:`yandex_music.ynison.models.ynison_state.UpdatePlayerQueueInject`):
            Обновить состояние проигрывания инжектируемой сущности (в oneof ``parameters``).
        update_session_params (:obj:`yandex_music.ynison.models.ynison_state.UpdateSessionParams`):
            Обновить информацию об устройстве-отправителе (в oneof ``parameters``).
        update_volume_info (:obj:`yandex_music.ynison.models.ynison_state.UpdateVolumeInfo`):
            Обновить громкость (в oneof ``parameters``).
        sync_state_from_eov (:obj:`yandex_music.ynison.models.ynison_state.SyncStateFromEOV`):
            Запросить синхронизацию с сервисом ЕОВ (в oneof ``parameters``).
        player_action_timestamp_ms (:obj:`int`): Время последнего изменения в плеере
            в миллисекундах.
        rid (:obj:`str`): Request id. Генерируется клиентом, используется для логирования и отладки.
        activity_interception_type (:obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequestActivityInterceptionType`):
            Тактика перехвата активности устройством-отправителем.
    """

    update_full_state: 'UpdateFullState' = betterproto.message_field(1, group='parameters')
    update_active_device: 'UpdateActiveDevice' = betterproto.message_field(2, group='parameters')
    update_playing_status: 'UpdatePlayingStatus' = betterproto.message_field(3, group='parameters')
    update_player_state: 'UpdatePlayerState' = betterproto.message_field(4, group='parameters')
    update_volume: 'UpdateVolume' = betterproto.message_field(5, group='parameters')
    update_player_queue_inject: 'UpdatePlayerQueueInject' = betterproto.message_field(6, group='parameters')
    update_session_params: 'UpdateSessionParams' = betterproto.message_field(9, group='parameters')
    update_volume_info: 'UpdateVolumeInfo' = betterproto.message_field(11, group='parameters')
    sync_state_from_eov: 'SyncStateFromEOV' = betterproto.message_field(12, group='parameters')
    player_action_timestamp_ms: int = betterproto.int64_field(7)
    rid: str = betterproto.string_field(8)
    activity_interception_type: 'PutYnisonStateRequestActivityInterceptionType' = betterproto.enum_field(10)


@dataclass
class PutYnisonStateResponse(betterproto.Message):
    """Класс, представляющий ответ сервера на обновление состояния Ynison.

    Сервер отправляет фрейм клиенту в трёх случаях: в ответ на ``PutYnisonStateRequest``,
    меняющий состояние на сервере; при обновлении на другом клиенте, которое нужно
    транслировать всем подключённым устройствам; при изменении списка устройств.

    Attributes:
        player_state (:obj:`yandex_music.ynison.models.ynison_state.PlayerState`):
            Состояние плеера.
        devices (:obj:`list` из :obj:`yandex_music.ynison.models.ynison_state.Device`):
            Список подключённых устройств.
        active_device_id_optional (:obj:`str`, optional): Идентификатор активного устройства.
        timestamp_ms (:obj:`int`): Время создания ответа сервера в миллисекундах.
        rid (:obj:`str`): Request id. Предположительно тот, который послужил причиной
            отправки ответа.
    """

    player_state: 'PlayerState' = betterproto.message_field(1)
    devices: List['Device'] = betterproto.message_field(2)
    active_device_id_optional: Optional[str] = betterproto.message_field(3, wraps=betterproto.TYPE_STRING)
    timestamp_ms: int = betterproto.int64_field(4)
    rid: str = betterproto.string_field(5)


@dataclass
class UpdatePlayerQueueInject(betterproto.Message):
    """Класс, представляющий обновление состояния инжектируемой в очередь сущности.

    Attributes:
        player_queue_inject (:obj:`yandex_music.ynison.models.ynison_state.PlayerQueueInject`):
            Состояние инжектируемой сущности.
    """

    player_queue_inject: 'PlayerQueueInject' = betterproto.message_field(1)


@dataclass
class UpdateActiveDevice(betterproto.Message):
    """Класс, представляющий обновление активного устройства.

    Отправляется при выборе пользователем устройства, которое должно проигрывать звук.

    Attributes:
        device_id_optional (:obj:`str`, optional): Идентификатор нового активного устройства.
    """

    device_id_optional: Optional[str] = betterproto.message_field(1, wraps=betterproto.TYPE_STRING)


@dataclass
class UpdatePlayingStatus(betterproto.Message):
    """Класс, представляющий обновление статуса воспроизведения.

    Отправляется при старте, паузе, перемотке или изменении скорости воспроизведения.

    Attributes:
        playing_status (:obj:`yandex_music.ynison.models.ynison_state.PlayingStatus`):
            Новый статус воспроизведения.
    """

    playing_status: 'PlayingStatus' = betterproto.message_field(1)


@dataclass
class UpdateVolume(betterproto.Message):
    """Класс, представляющий обновление уровня громкости (устаревший).

    См. :class:`UpdateVolumeInfo`.

    Attributes:
        volume (:obj:`float`): Громкость в интервале ``[0; 1]``.
        device_id (:obj:`str`): Идентификатор устройства, на котором меняется громкость.
    """

    volume: float = betterproto.double_field(1)
    device_id: str = betterproto.string_field(2)


@dataclass
class UpdateVolumeInfo(betterproto.Message):
    """Класс, представляющий обновление громкости устройства.

    Attributes:
        device_id (:obj:`str`): Идентификатор устройства, на котором меняется громкость.
        volume_info (:obj:`yandex_music.ynison.models.ynison_state.DeviceVolume`):
            Новое значение состояния громкости с версией изменений.
    """

    device_id: str = betterproto.string_field(1)
    volume_info: 'DeviceVolume' = betterproto.message_field(2)


@dataclass
class UpdatePlayerState(betterproto.Message):
    """Класс, представляющий обновление состояния плеера.

    Отправляется при старте новой очереди, её обновлении (добавление/удаление сущности)
    и изменении режима повтора/шаффла.

    Attributes:
        player_state (:obj:`yandex_music.ynison.models.ynison_state.PlayerState`):
            Новое состояние воспроизведения.
    """

    player_state: 'PlayerState' = betterproto.message_field(1)


@dataclass
class UpdateFullState(betterproto.Message):
    """Класс, представляющий обновление полного состояния проигрывания и устройств.

    Отправляется при холодном старте, выключении оффлайн-режима и появлении сети после
    её отключения.

    Attributes:
        player_state (:obj:`yandex_music.ynison.models.ynison_state.PlayerState`):
            Состояние плеера.
        is_currently_active (:obj:`bool`): Является ли устройство активным (играет звук).
        device (:obj:`yandex_music.ynison.models.ynison_state.UpdateDevice`):
            Информация об устройстве.
        sync_state_from_eov_optional (:obj:`yandex_music.ynison.models.ynison_state.SyncStateFromEOV`):
            Запрос синхронизации с сервисом ЕОВ во время обработки ``UpdateFullState``.
            Если не передан — синхронизация будет вызвана только для сценариев холодного старта.
    """

    player_state: 'PlayerState' = betterproto.message_field(1)
    is_currently_active: bool = betterproto.bool_field(2)
    device: 'UpdateDevice' = betterproto.message_field(3)
    sync_state_from_eov_optional: 'SyncStateFromEOV' = betterproto.message_field(4)


@dataclass
class UpdateSessionParams(betterproto.Message):
    """Класс, представляющий обновление поведения сервера в отношении устройства в рамках сессии.

    Параметры сбрасываются при переподключении.

    Attributes:
        mute_events_if_passive (:obj:`bool`): Пока устройство находится в пассивном режиме,
            оно не будет получать с сервера новые события. Флаг сбрасывается, если текущее
            устройство становится активным. Если устройство уже активно, флаг игнорируется.
    """

    mute_events_if_passive: bool = betterproto.bool_field(1)


@dataclass
class UpdateDevice(betterproto.Message):
    """Класс, представляющий информацию об устройстве, передаваемую самим устройством на сервер.

    Attributes:
        info (:obj:`yandex_music.ynison.models.ynison_state.DeviceInfo`):
            Информация об устройстве.
        volume (:obj:`float`): Громкость. Устаревшее, см. ``volume_info``.
        capabilities (:obj:`yandex_music.ynison.models.ynison_state.DeviceCapabilities`):
            Настройки доступности.
        volume_info (:obj:`yandex_music.ynison.models.ynison_state.DeviceVolume`):
            Громкость устройства.
    """

    info: 'DeviceInfo' = betterproto.message_field(1)
    volume: float = betterproto.double_field(2)
    capabilities: 'DeviceCapabilities' = betterproto.message_field(3)
    volume_info: 'DeviceVolume' = betterproto.message_field(4)


@dataclass
class SyncStateFromEOV(betterproto.Message):
    """Класс, представляющий запрос синхронизации с сервисом ЕОВ (единой очереди воспроизведения).

    Запрос синхронизации может быть отклонён сервером, если текущее устройство не активно
    и не получило активности в результате вызова этого метода.

    Сценарий обновления:

    1. Бэкенд проверяет активность устройства и делает его активным, если требуется
       (см. :class:`PutYnisonStateRequestActivityInterceptionType`).
    2. Если устройство не является активным после шага 1, команда тихо игнорируется.
    3. Бэкенд получает список очередей из ЕОВ.
    4. Если id последней очереди в списке совпадает с ``actual_queue_id``, обновление не
       произойдёт — переход к пункту 6.
    5. Пробуем обновить стейт на основании ЕОВ. Новое состояние плеера будет содержать
       ``[UpdateVersion#device_id]``, отличный от id устройства-отправителя.
    6. Если стейт был обновлён или сменилось активное устройство — рассылаем эвент всем
       устройствам. Иначе выходим без событий и ошибок.

    Attributes:
        actual_queue_id (:obj:`str`): Идентификатор очереди устройства в ЕОВ. Пустая строка —
            допустимое значение, если клиент не имеет информации о синхронизации очередей.
    """

    actual_queue_id: str = betterproto.string_field(1)
