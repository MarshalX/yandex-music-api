##############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/radio.py. DON'T EDIT IT BY HANDS #
##############################################################################################

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import Dashboard, StationResult, StationTracksResult, Status
from yandex_music._client import log
from yandex_music._client_base import ClientBase, TimestampType

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class RadioMixin(ClientBase):
    """Миксин для методов, связанных с радио (rotor)."""

    _request: 'Request'

    @log
    def rotor_account_status(self, *args: Any, **kwargs: Any) -> Optional[Status]:
        """Получение статуса пользователя с дополнительными полями.

        Note:
            Данный статус отличается от обычного наличием дополнительных полей, например, `skips_per_hour`.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Status` | :obj:`None`: Статус пользователя с дополнительными полями от радио или
                :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/account/status'

        result = self._request.get(url, *args, **kwargs)

        return Status.de_json(result, self)

    @log
    def rotor_stations_dashboard(self, *args: Any, **kwargs: Any) -> Optional[Dashboard]:
        """Получение рекомендованных станций текущего пользователя.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Dashboard` | :obj:`None`: Рекомендованные станции или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/stations/dashboard'

        result = self._request.get(url, *args, **kwargs)

        return Dashboard.de_json(result, self)

    @log
    def rotor_stations_list(self, language: Optional[str] = None, *args: Any, **kwargs: Any) -> List[StationResult]:
        """Получение всех радиостанций с настройками пользователя.

        Note:
            Доступные языки: en, uz, uk, us, ru, kk, hy.

            Чтобы определить что за тип станции (жанры, настроения, занятие и т.д.) необходимо смотреть в поле
            `id_for_from`.

        Args:
            language (:obj:`str`, optional): Язык, на котором будет информация о станциях. По умолчанию язык клиента.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.StationResult`: Список станций.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/stations/list'

        if not language:
            language = self.language

        result = self._request.get(url, {'language': language}, *args, **kwargs)

        return list(StationResult.de_list(result, self))

    @log
    def rotor_station_feedback(
        self,
        station: str,
        type_: str,
        timestamp: TimestampType = None,
        from_: Optional[str] = None,
        batch_id: Optional[str] = None,
        total_played_seconds: Optional[Union[int, float]] = None,
        track_id: Optional[Union[str, int]] = None,
        **kwargs: Any,
    ) -> bool:
        """Отправка обратной связи на действия при прослушивании радио.

        Note:
            Сообщения о начале прослушивания радио, начале и конце трека, его пропуска.

            Известные типы обратной связи: `radioStarted`, `trackStarted`, `trackFinished`, `skip`.

            Пример `station`: `user:onyourwave`, `genre:allrock`.

            Пример `from_`: `mobile-radio-user-123456789`.

        Args:
            station (:obj:`str`): Станция.
            type_ (:obj:`str`): Тип отправляемого отзыва.
            timestamp (:obj:`str` | :obj:`float` | :obj:`int`, optional): Текущее время и дата.
            from_ (:obj:`str`, optional): Откуда начато воспроизведение радио.
            batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков. Возвращается при получении треков.
            total_played_seconds (:obj:`int` |:obj:`float`, optional): Сколько было проиграно секунд трека
                перед действием.
            track_id (:obj:`int` | :obj:`str`, optional): Уникальной идентификатор трека.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if timestamp is None:
            timestamp = datetime.now().timestamp()

        url = f'{self.base_url}/rotor/station/{station}/feedback'

        params = {}
        data = {'type': type_, 'timestamp': timestamp}

        if batch_id:
            params = {'batch-id': batch_id}

        if track_id:
            data.update({'trackId': track_id})

        if from_:
            data.update({'from': from_})

        if total_played_seconds:
            data.update({'totalPlayedSeconds': total_played_seconds})

        result = self._request.post(url, params=params, data=data, **kwargs)

        return result == 'ok'

    @log
    def rotor_station_feedback_radio_started(
        self,
        station: str,
        from_: str,
        batch_id: Optional[str] = None,
        timestamp: TimestampType = None,
        **kwargs: Any,
    ) -> bool:
        """Сокращение для::

            client.rotor_station_feedback(station, 'radioStarted', timestamp, from, batch_id, **kwargs)

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self.rotor_station_feedback(station, 'radioStarted', timestamp, from_=from_, batch_id=batch_id, **kwargs)

    @log
    def rotor_station_feedback_track_started(
        self,
        station: str,
        track_id: Union[str, int],
        batch_id: Optional[str] = None,
        timestamp: TimestampType = None,
        **kwargs: Any,
    ) -> bool:
        """Сокращение для::

            client.rotor_station_feedback(station, 'trackStarted', timestamp, track_id=track_id,
            batch_id=batch_id, **kwargs)

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self.rotor_station_feedback(
            station, 'trackStarted', timestamp, track_id=track_id, batch_id=batch_id, **kwargs
        )

    @log
    def rotor_station_feedback_track_finished(
        self,
        station: str,
        track_id: Union[str, int],
        total_played_seconds: float,
        batch_id: Optional[str] = None,
        timestamp: TimestampType = None,
        **kwargs: Any,
    ) -> bool:
        """Сокращение для::

            client.rotor_station_feedback(station, 'trackFinished', timestamp,
            track_id=track_id, total_played_seconds=total_played_seconds, batch_id=batch_id, **kwargs)

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self.rotor_station_feedback(
            station,
            'trackFinished',
            timestamp,
            track_id=track_id,
            total_played_seconds=total_played_seconds,
            batch_id=batch_id,
            **kwargs,
        )

    @log
    def rotor_station_feedback_skip(
        self,
        station: str,
        track_id: Union[str, int],
        total_played_seconds: float,
        batch_id: Optional[str] = None,
        timestamp: TimestampType = None,
        **kwargs: Any,
    ) -> bool:
        """Сокращение для::

            client.rotor_station_feedback(station, 'skip', timestamp, track_id=track_id,
            total_played_seconds=total_played_seconds, batch_id=batch_id, **kwargs)

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self.rotor_station_feedback(
            station,
            'skip',
            timestamp,
            track_id=track_id,
            total_played_seconds=total_played_seconds,
            batch_id=batch_id,
            **kwargs,
        )

    @log
    def rotor_station_info(self, station: str, *args: Any, **kwargs: Any) -> List[StationResult]:
        """Получение информации о станции и пользовательских настроек на неё.

        Args:
            station (:obj:`str`): Станция.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.StationResult` | :obj:`None`: Информация о станции или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/station/{station}/info'

        result = self._request.get(url, *args, **kwargs)

        return list(StationResult.de_list(result, self))

    @log
    def rotor_station_settings2(
        self,
        station: str,
        mood_energy: str,
        diversity: str,
        language: str = 'not-russian',  # TODO(#555): заменить на any
        type_: str = 'rotor',
        **kwargs: Any,
    ) -> bool:
        """Изменение настроек определённой станции.

        Note:
            Доступные значения для `mood_energy`: `fun`, `active`, `calm`, `sad`, `all`.

            Доступные значения для `diversity`: `favorite`, `popular`, `discover`, `default`.

            Доступные значения для `language`: `not-russian`, `russian`, `any`.

            Доступные значения для `type_`: `rotor`, `generative`.

            У станций в `restrictions` есть Enum'ы, а в них `possible_values` - доступные значения для поля.

        Args:
            station (:obj:`str`): Станция.
            mood_energy (:obj:`str`): Настроение.
            diversity (:obj:`str`): Треки.
            language (:obj:`str`): Язык.
            type_ (:obj:`str`): Тип.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/station/{station}/settings3'

        data = {'moodEnergy': mood_energy, 'diversity': diversity, 'type': type_}

        if language:
            data.update({'language': language})

        result = self._request.post(url, data=data, **kwargs)

        return result == 'ok'

    @log
    def rotor_station_tracks(
        self,
        station: str,
        settings2: bool = True,
        queue: Optional[Union[str, int]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[StationTracksResult]:
        """Получение цепочки треков определённой станции.

        Note:
            Запуск потока по сущности сервиса осуществляется через станцию `<type>:<id>`.
            Например, станцией для запуска потока по треку будет `track:1234`.

            Для продолжения цепочки треков необходимо:

            1. Передавать `ID` трека, что был до этого (первый в цепочки).
            2. Отправить фидбек о конце или скипе трека, что был передан в `queue`.
            3. Отправить фидбек о начале следующего трека (второй в цепочки).
            4. Выполнить запрос получения треков. В ответе придёт новые треки или произойдёт сдвиг цепочки на 1 элемент.

            Проход по цепочке до конца не изучен. Часто встречаются дубликаты.

            Все официальные клиенты выполняют запросы с `settings2 = True`.

        Args:
            station (:obj:`str`): Станция.
            settings2 (:obj:`bool`, optional): Использовать ли второй набор настроек.
            queue (:obj:`str` | :obj:`int`, optional): Уникальной идентификатор трека, который только что был.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.StationTracksResult` | :obj:`None`: Последовательность треков станции или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/station/{station}/tracks'

        params = {}
        if settings2:
            params = {'settings2': str(True)}

        if queue:
            params = {'queue': queue}

        result = self._request.get(url, params, *args, **kwargs)

        return StationTracksResult.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`rotor_account_status`
    rotorAccountStatus = rotor_account_status
    #: Псевдоним для :attr:`rotor_stations_dashboard`
    rotorStationsDashboard = rotor_stations_dashboard
    #: Псевдоним для :attr:`rotor_stations_list`
    rotorStationsList = rotor_stations_list
    #: Псевдоним для :attr:`rotor_station_feedback`
    rotorStationFeedback = rotor_station_feedback
    #: Псевдоним для :attr:`rotor_station_feedback_radio_started`
    rotorStationFeedbackRadioStarted = rotor_station_feedback_radio_started
    #: Псевдоним для :attr:`rotor_station_feedback_track_started`
    rotorStationFeedbackTrackStarted = rotor_station_feedback_track_started
    #: Псевдоним для :attr:`rotor_station_feedback_track_finished`
    rotorStationFeedbackTrackFinished = rotor_station_feedback_track_finished
    #: Псевдоним для :attr:`rotor_station_feedback_skip`
    rotorStationFeedbackSkip = rotor_station_feedback_skip
    #: Псевдоним для :attr:`rotor_station_info`
    rotorStationInfo = rotor_station_info
    #: Псевдоним для :attr:`rotor_station_settings2`
    rotorStationSettings2 = rotor_station_settings2
    #: Псевдоним для :attr:`rotor_station_tracks`
    rotorStationTracks = rotor_station_tracks
