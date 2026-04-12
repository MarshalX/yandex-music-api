from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from typing_extensions import Self

from yandex_music import Experiments, PermissionAlerts, PromoCodeStatus, Settings, Status, UserSettings
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class AccountMixin(ClientBase):
    """Миксин для методов, связанных с аккаунтом и настройками."""

    _request: 'Request'

    @log
    async def init(self, *args, **kwargs) -> Self:
        """Получение информации об аккаунте, использующейся в других запросах.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ClientAsync`: клиент Yandex Music.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        self.me = await self.account_status(*args, **kwargs)
        if self.me and self.me.account:
            self.account_uid = self.me.account.uid
        return self

    @log
    async def account_status(self, *args: Any, **kwargs: Any) -> Optional[Status]:
        """Получение статуса аккаунта. Нет обязательных параметров.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Status` | :obj:`None`: Информация об аккаунте если он валиден, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/account/status'

        result = await self._request.get(url, *args, **kwargs)

        return Status.de_json(result, self)

    @log
    async def account_settings(self, *args: Any, **kwargs: Any) -> Optional[UserSettings]:
        """Получение настроек текущего пользователя.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.UserSettings` | :obj:`None`: Настройки пользователя если аккаунт валиден,
                иначе :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/account/settings'

        result = await self._request.get(url, *args, **kwargs)

        return UserSettings.de_json(result, self)

    @log
    async def account_settings_set(
        self,
        param: Optional[str] = None,
        value: Optional[Union[str, int, bool]] = None,
        data: Optional[Dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[UserSettings]:
        """Изменение настроек текущего пользователя.

        Note:
            Доступные названия параметров есть поля в классе :class:`yandex_music.UserSettings`, только в CamelCase.

        Args:
            param (:obj:`str`): Название параметра для изменения.
            value (:obj:`str` | :obj:`int` | :obj:`bool`): Значение параметра.
            data (:obj:`dict`): Словарь параметров и значений для множественного изменения.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.UserSettings` | :obj:`None`: Настройки пользователя или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/account/settings'

        if not data and param:
            data = {param: str(value)}

        result = await self._request.post(url, data, *args, **kwargs)

        return UserSettings.de_json(result, self)

    @log
    async def settings(self, *args: Any, **kwargs: Any) -> Optional[Settings]:
        """Получение предложений по покупке. Нет обязательных параметров.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Settings` | :obj:`None`: Информацию о предлагаемых продуктах если аккаунт валиден
                или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/settings'

        result = await self._request.get(url, *args, **kwargs)

        return Settings.de_json(result, self)

    @log
    async def permission_alerts(self, *args: Any, **kwargs: Any) -> Optional[PermissionAlerts]:
        """Получение оповещений. Нет обязательных параметров.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PermissionAlerts` | :obj:`None`: Оповещения если аккаунт валиден или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/permission-alerts'

        result = await self._request.get(url, *args, **kwargs)

        return PermissionAlerts.de_json(result, self)

    @log
    async def account_experiments(self, *args: Any, **kwargs: Any) -> Optional[Experiments]:
        """Получение значений экспериментальных функций аккаунта.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Experiments` | :obj:`None`: Состояние экспериментальных функций или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/account/experiments'

        result = await self._request.get(url, *args, **kwargs)

        return Experiments.de_json(result, self)

    @log
    async def consume_promo_code(
        self, code: str, language: Optional[str] = None, *args, **kwargs
    ) -> Optional[PromoCodeStatus]:
        """Активация промо-кода.

        Note:
            Доступные языки: en, uz, uk, us, ru, kk, hy.

        Args:
            code (:obj:`str`): Промо-код.
            language (:obj:`str`, optional): Язык ответа API в ISO 639-1. По умолчанию язык клиента.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PromoCodeStatus` | :obj:`None`: Информация об активации промо-кода или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/account/consume-promo-code'

        if not language:
            language = self.language

        result = await self._request.post(url, {'code': code, 'language': language}, *args, **kwargs)

        return PromoCodeStatus.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`account_status`
    accountStatus = account_status
    #: Псевдоним для :attr:`account_settings`
    accountSettings = account_settings
    #: Псевдоним для :attr:`account_settings_set`
    accountSettingsSet = account_settings_set
    #: Псевдоним для :attr:`permission_alerts`
    permissionAlerts = permission_alerts
    #: Псевдоним для :attr:`account_experiments`
    accountExperiments = account_experiments
    #: Псевдоним для :attr:`consume_promo_code`
    consumePromoCode = consume_promo_code
