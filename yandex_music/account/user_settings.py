from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class UserSettings(YandexMusicObject):
    """Класс, предоставляющий настройки пользователя.

    Доступные значения для поля `theme`: `white`, `black`.
    Доступные значения для полей `user_music_visibility` и `user_social_visibility`: `private`, `public`.

    Attributes:
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 uid: int,
                 last_fm_scrobbling_enabled: bool,
                 shuffle_enabled: bool,
                 volume_percents: int,
                 modified: str,
                 facebook_scrobbling_enabled: bool,
                 add_new_track_on_playlist_top: bool,
                 user_music_visibility: str,
                 user_social_visibility: str,
                 rbt_disabled: bool,
                 theme: str,
                 promos_disabled: bool,
                 auto_play_radio: bool,
                 ads_disabled: Optional[bool] = None,
                 disk_enabled: Optional[bool] = None,
                 show_disk_tracks_in_library: Optional[bool] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.uid = uid
        self.last_fm_scrobbling_enabled = last_fm_scrobbling_enabled
        self.shuffle_enabled = shuffle_enabled
        self.volume_percents = volume_percents
        self.modified = modified
        self.facebook_scrobbling_enabled = facebook_scrobbling_enabled
        self.add_new_track_on_playlist_top = add_new_track_on_playlist_top
        self.user_music_visibility = user_music_visibility
        self.user_social_visibility = user_social_visibility
        self.rbt_disabled = rbt_disabled
        self.theme = theme
        self.promos_disabled = promos_disabled
        self.auto_play_radio = auto_play_radio

        self.ads_disabled = ads_disabled
        self.disk_enabled = disk_enabled
        self.show_disk_tracks_in_library = show_disk_tracks_in_library

        self.client = client
        self._id_attrs = (self.uid, )

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['UserSettings']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.UserSettings`: Объект класса :class:`yandex_music.UserSettings`.
        """
        if not data:
            return None

        data = super(UserSettings, cls).de_json(data, client)

        return cls(client=client, **data)
