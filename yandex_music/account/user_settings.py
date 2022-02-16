from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class UserSettings(YandexMusicObject):
    """Класс, представляющий настройки пользователя.

    Note:
        Доступные значения для поля `theme`: `white`, `black`.

        Доступные значения для полей `user_music_visibility` и `user_social_visibility`: `private`, `public`.

    Notes:
        `promos_disabled`, `ads_disabled`, `rbt_disabled` устарели и не работают.

        `last_fm_scrobbling_enabled`, `facebook_scrobbling_enabled` выглядят устаревшими.

    Attributes:
        uid (:obj:`int`): Уникальный идентификатор пользователя.
        last_fm_scrobbling_enabled (:obj:`bool`): Скробблинг lastfm.
        shuffle_enabled (:obj:`bool`): Переключать треки в случайном порядке.
        volume_percents (:obj:`int`): Громкость звука в процентах.
        modified (:obj:`str`): Дата изменения настроек.
        facebook_scrobbling_enabled (:obj:`bool`): Скробблинг facebook.
        add_new_track_on_playlist_top (:obj:`bool`): Добавлять новые треки в начало плейлиста.
        user_music_visibility (:obj:`str`): Публичный доступ к моей фонотеке.
        user_social_visibility (:obj:`str`): Показывать соцсети на странице.
        rbt_disabled (:obj:`bool`): TODO (неиспользуемая фича).
        theme (:obj:`str`): Тема оформления.
        promos_disabled (:obj:`bool`): Не показывать рекламируемый контент).
        auto_play_radio (:obj:`bool`): Бесконечный поток музыки.
        sync_queue_enabled (:obj:`bool`): Синхронизация очередей между устройствами.
        ads_disabled (:obj:`bool`, optional): Не показывать рекламу.
        disk_enabled (:obj:`bool`, optional): TODO.
        show_disk_tracks_in_library (:obj:`bool`, optional): Показывать локальные треки в библиотеке.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    uid: int
    last_fm_scrobbling_enabled: bool
    shuffle_enabled: bool
    volume_percents: int
    modified: str
    facebook_scrobbling_enabled: bool
    add_new_track_on_playlist_top: bool
    user_music_visibility: str
    user_social_visibility: str
    rbt_disabled: bool
    theme: str
    promos_disabled: bool
    auto_play_radio: bool
    sync_queue_enabled: bool
    ads_disabled: Optional[bool] = None
    disk_enabled: Optional[bool] = None
    show_disk_tracks_in_library: Optional[bool] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (
            self.uid,
            self.last_fm_scrobbling_enabled,
            self.shuffle_enabled,
            self.volume_percents,
            self.modified,
            self.facebook_scrobbling_enabled,
            self.add_new_track_on_playlist_top,
            self.user_music_visibility,
            self.user_social_visibility,
            self.rbt_disabled,
            self.theme,
            self.promos_disabled,
            self.auto_play_radio,
            self.sync_queue_enabled,
            self.ads_disabled,
            self.disk_enabled,
            self.show_disk_tracks_in_library,
        )

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['UserSettings']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.UserSettings`: Настройки пользователя.
        """
        if not data:
            return None

        data = super(UserSettings, cls).de_json(data, client)

        return cls(client=client, **data)
