#############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/wave.py. DON'T EDIT IT BY HANDS #
#############################################################################################

from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import Wave, WaveSettings
from yandex_music._client import log
from yandex_music._client_base import ClientBase, is_dict

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class WaveMixin(ClientBase):
    """Волна.

    Миксин для методов, связанных с волной (последняя волна пользователя и её настройки).
    """

    _request: 'Request'

    @log
    def rotor_wave_last(self, *args: Any, **kwargs: Any) -> Optional[Wave]:
        """Получение последней запущенной волны пользователя.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Wave` | :obj:`None`: Последняя волна или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/wave/last'

        result = self._request.get(url, *args, **kwargs)

        return Wave.de_json(result, self)

    @log
    def rotor_wave_last_reset(self, **kwargs: Any) -> bool:
        """Сброс последней запущенной волны пользователя на «Мою волну».

        Args:
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/wave/last/reset'

        result = self._request.post(url, **kwargs)

        return is_dict(result) and result.get('result') == 'ok'

    @log
    def rotor_wave_settings(
        self, seeds: Optional[Union[str, List[str]]] = None, *args: Any, **kwargs: Any
    ) -> Optional[WaveSettings]:
        """Получение настроек волны: контекстов (занятий) и доступных значений настроек.

        Args:
            seeds (:obj:`str` | :obj:`list` из :obj:`str`, optional): Сиды волны (например, `user:onyourwave`).
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.WaveSettings` | :obj:`None`: Настройки волны или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/wave/settings'

        params = {}
        if seeds:
            params['seeds'] = seeds if isinstance(seeds, str) else ','.join(seeds)

        result = self._request.get(url, params, *args, **kwargs)

        return WaveSettings.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`rotor_wave_last`
    rotorWaveLast = rotor_wave_last
    #: Псевдоним для :attr:`rotor_wave_last_reset`
    rotorWaveLastReset = rotor_wave_last_reset
    #: Псевдоним для :attr:`rotor_wave_settings`
    rotorWaveSettings = rotor_wave_settings
