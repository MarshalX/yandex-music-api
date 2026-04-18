#######################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/client_async.py. DON'T EDIT IT BY HANDS #
#######################################################################################

import logging
from typing import Optional

from yandex_music import Status, YandexMusicObject, __copyright__, __license__, __version__
from yandex_music._client.account import AccountMixin
from yandex_music._client.albums import AlbumsMixin
from yandex_music._client.artists import ArtistsMixin
from yandex_music._client.clips import ClipsMixin
from yandex_music._client.concerts import ConcertsMixin
from yandex_music._client.credits import CreditsMixin
from yandex_music._client.device_auth import DeviceAuthMixin
from yandex_music._client.disclaimers import DisclaimersMixin
from yandex_music._client.labels import LabelsMixin
from yandex_music._client.landing import LandingMixin
from yandex_music._client.likes import LikesMixin
from yandex_music._client.metatags import MetatagsMixin
from yandex_music._client.music_history import MusicHistoryMixin
from yandex_music._client.pins import PinsMixin
from yandex_music._client.playlists import PlaylistsMixin
from yandex_music._client.presaves import PresavesMixin
from yandex_music._client.queue import QueueMixin
from yandex_music._client.radio import RadioMixin
from yandex_music._client.search import SearchMixin
from yandex_music._client.tracks import TracksMixin
from yandex_music.utils.request import Request

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Client(
    AccountMixin,
    AlbumsMixin,
    ClipsMixin,
    ConcertsMixin,
    CreditsMixin,
    DeviceAuthMixin,
    DisclaimersMixin,
    LabelsMixin,
    LandingMixin,
    TracksMixin,
    SearchMixin,
    PlaylistsMixin,
    RadioMixin,
    ArtistsMixin,
    LikesMixin,
    MetatagsMixin,
    MusicHistoryMixin,
    PinsMixin,
    PresavesMixin,
    QueueMixin,
    YandexMusicObject,
):
    """Класс, представляющий клиент Yandex Music.

    Note:
        Доступные языки: en, uz, uk, us, ru, kk, hy.

        Поле `device` используется только при работе с очередью прослушивания.

    Attributes:
        logger (:obj:`logging.Logger`): Объект логгера.
        token (:obj:`str`): Уникальный ключ для аутентификации.
        base_url (:obj:`str`): Ссылка на API Yandex Music.
        me (:obj:`yandex_music.Status`): Информация об аккаунте.
        device (:obj:`str`): Строка, содержащая сведения об устройстве, с которого выполняются запросы.
        report_unknown_fields (:obj:`bool`): Включены ли предупреждения о неизвестных полях от API,
            которых нет в библиотеке.

    Args:
        token (:obj:`str`, optional): Уникальный ключ для аутентификации.
        base_url (:obj:`str`, optional): Ссылка на API Yandex Music.
        request (:obj:`yandex_music.utils.request.Request`, optional): Пре-инициализация
            :class:`yandex_music.utils.request.Request`.
        language (:obj:`str`, optional): Язык, на котором будут приходить ответы от API. По умолчанию русский.
        report_unknown_fields (:obj:`bool`, optional): Включить предупреждения о неизвестных полях от API,
            которых нет в библиотеке.
    """

    __notice_displayed = True  # больше не используется

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
        request: Optional[Request] = None,
        language: str = 'ru',
        report_unknown_fields: bool = False,
    ) -> None:
        if not Client.__notice_displayed:
            print(f'Yandex Music API v{__version__}, {__copyright__}')
            print(f'Licensed under the terms of the {__license__}', end='\n\n')
            Client.__notice_displayed = True

        self.logger = logging.getLogger(__name__)
        self.token = token

        if base_url is None:
            base_url = 'https://api.music.yandex.net'

        self.base_url = base_url

        self.report_unknown_fields = report_unknown_fields

        if request:
            self._request = request
            self._request.set_and_return_client(self)
        else:
            self._request = Request(self)

        self.language = language
        self._request.set_language(self.language)

        self.device = (
            'os=Python; os_version=; manufacturer=Marshal; model=Yandex Music API; clid=; device_id=random; uuid=random'
        )

        self.me: Optional['Status'] = None
        self.account_uid: Optional[int] = None

    @property
    def request(self) -> Request:
        """:obj:`yandex_music.utils.request.Request`: Объект вспомогательного класса для отправки запросов."""
        return self._request
