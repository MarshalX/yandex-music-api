from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from yandex_music import (
    CombinedSession,
    CombinedSessionLanding,
    CombinedSessionQueueItem,
    RotorSession,
    RotorSessionTracks,
    SessionEvent,
    SessionFeedback,
    SessionFeedbacks,
)
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase, TimestampType, is_dict, utc_now_iso

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


def _session_body(
    queue: Optional[List[str]],
    track_to_start_from: Optional[str],
    include_tracks_in_response: Optional[bool],
    include_wave_model: Optional[bool],
    interactive: Optional[bool],
    incognito: Optional[bool],
    child: Optional[bool],
    allow_explicit: Optional[bool],
) -> Dict[str, Any]:
    body = {
        'queue': queue,
        'trackToStartFrom': track_to_start_from,
        'includeTracksInResponse': include_tracks_in_response,
        'includeWaveModel': include_wave_model,
        'interactive': interactive,
        'incognito': incognito,
        'child': child,
        'allowExplicit': allow_explicit,
    }

    return {key: value for key, value in body.items() if value is not None}


class RotorSessionsMixin(ClientBase):
    """Сессии радио.

    Миксин для методов, связанных с сессиями радио (rotor session) и комбинированными сессиями (треки и клипы).

    Note:
        Сессия является актуальным способом слушать радио: она создаётся по сидам, выдаёт партии треков и принимает
        обратную связь о прослушивании.
    """

    _request: 'Request'

    @log
    async def rotor_session_new(
        self,
        seeds: Union[str, List[str]],
        queue: Optional[List[str]] = None,
        track_to_start_from: Optional[str] = None,
        include_tracks_in_response: Optional[bool] = None,
        include_wave_model: Optional[bool] = None,
        interactive: Optional[bool] = None,
        incognito: Optional[bool] = None,
        child: Optional[bool] = None,
        allow_explicit: Optional[bool] = None,
        **kwargs: Any,
    ) -> Optional[RotorSession]:
        """Создание новой сессии радио.

        Note:
            Пример `seeds`: `user:onyourwave`, `genre:rock`, `track:12345`, `artist:12345`.
            В качестве сидов можно передавать и настройки волны, например, `settingDiversity:discover`
            (см. :attr:`yandex_music.Value.serialized_seed`).

            Треки (`track_to_start_from`, `queue`) передаются как `id` или `id:album_id`.

        Args:
            seeds (:obj:`str` | :obj:`list` из :obj:`str`): Сиды сессии.
            queue (:obj:`list` из :obj:`str`, optional): Уже проигранные треки, чтобы не получить их повторно.
            track_to_start_from (:obj:`str`, optional): Трек, с которого начать сессию.
            include_tracks_in_response (:obj:`bool`, optional): Возвращать ли треки в ответе. По умолчанию
                на стороне API да.
            include_wave_model (:obj:`bool`, optional): Возвращать ли модель волны (:attr:`RotorSession.wave`).
            interactive (:obj:`bool`, optional): Интерактивная ли сессия.
            incognito (:obj:`bool`, optional): Не учитывать прослушивания в рекомендациях.
            child (:obj:`bool`, optional): Детский режим.
            allow_explicit (:obj:`bool`, optional): Разрешить ли контент с ненормативной лексикой.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.RotorSession` | :obj:`None`: Сессия радио или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/session/new'

        body = _session_body(
            queue,
            track_to_start_from,
            include_tracks_in_response,
            include_wave_model,
            interactive,
            incognito,
            child,
            allow_explicit,
        )
        body['seeds'] = [seeds] if isinstance(seeds, str) else seeds

        result = await self._request.post(url, json=body, **kwargs)

        return RotorSession.de_json(result, self)

    @log
    async def rotor_session_clone(
        self,
        radio_session_id: str,
        queue: Optional[List[str]] = None,
        track_to_start_from: Optional[str] = None,
        include_tracks_in_response: Optional[bool] = None,
        include_wave_model: Optional[bool] = None,
        interactive: Optional[bool] = None,
        incognito: Optional[bool] = None,
        child: Optional[bool] = None,
        allow_explicit: Optional[bool] = None,
        **kwargs: Any,
    ) -> Optional[RotorSession]:
        """Создание новой сессии радио на основе существующей (с теми же сидами).

        Args:
            radio_session_id (:obj:`str`): Уникальный идентификатор исходной сессии.
            queue (:obj:`list` из :obj:`str`, optional): Уже проигранные треки, чтобы не получить их повторно.
            track_to_start_from (:obj:`str`, optional): Трек, с которого начать сессию.
            include_tracks_in_response (:obj:`bool`, optional): Возвращать ли треки в ответе.
            include_wave_model (:obj:`bool`, optional): Возвращать ли модель волны.
            interactive (:obj:`bool`, optional): Интерактивная ли сессия.
            incognito (:obj:`bool`, optional): Не учитывать прослушивания в рекомендациях.
            child (:obj:`bool`, optional): Детский режим.
            allow_explicit (:obj:`bool`, optional): Разрешить ли контент с ненормативной лексикой.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.RotorSession` | :obj:`None`: Новая сессия радио или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/session/{radio_session_id}/clone'

        body = _session_body(
            queue,
            track_to_start_from,
            include_tracks_in_response,
            include_wave_model,
            interactive,
            incognito,
            child,
            allow_explicit,
        )

        result = await self._request.post(url, json=body, **kwargs)

        return RotorSession.de_json(result, self)

    @log
    async def rotor_session_tracks(
        self,
        radio_session_id: str,
        queue: Optional[List[str]] = None,
        feedbacks: Optional[List[SessionFeedback]] = None,
        **kwargs: Any,
    ) -> Optional[RotorSessionTracks]:
        """Получение следующей партии треков сессии радио.

        Note:
            Для несуществующей сессии API не возвращает ошибку, а выставляет
            :attr:`yandex_music.RotorSessionTracks.unknown_session`.

        Args:
            radio_session_id (:obj:`str`): Уникальный идентификатор сессии.
            queue (:obj:`list` из :obj:`str`, optional): Уже полученные треки (`id` или `id:album_id`),
                чтобы не получить их повторно.
            feedbacks (:obj:`list` из :obj:`yandex_music.SessionFeedback`, optional): Обратная связь,
                отправляемая вместе с запросом.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.RotorSessionTracks` | :obj:`None`: Партия треков или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/session/{radio_session_id}/tracks'

        body: Dict[str, Any] = {'queue': queue or []}
        if feedbacks:
            body['feedbacks'] = [feedback.to_dict(for_request=True) for feedback in feedbacks]

        result = await self._request.post(url, json=body, **kwargs)

        return RotorSessionTracks.de_json(result, self)

    @log
    async def rotor_session_feedback(
        self,
        radio_session_id: str,
        event: SessionEvent,
        batch_id: Optional[str] = None,
        from_: Optional[str] = None,
        **kwargs: Any,
    ) -> bool:
        """Отправка обратной связи сессии радио.

        Note:
            Обязательные поля события зависят от его типа, см. :class:`yandex_music.SessionEvent`.

            Для частых событий есть отдельные методы: :func:`rotor_session_feedback_radio_started`,
            :func:`rotor_session_feedback_track_started`, :func:`rotor_session_feedback_track_finished`,
            :func:`rotor_session_feedback_skip`.

        Args:
            radio_session_id (:obj:`str`): Уникальный идентификатор сессии.
            event (:obj:`yandex_music.SessionEvent`): Событие.
            batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
            from_ (:obj:`str`, optional): Откуда начато воспроизведение.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/session/{radio_session_id}/feedback'

        feedback = SessionFeedback(event, batch_id, from_)

        result = await self._request.post(url, json=feedback.to_dict(for_request=True), **kwargs)

        return is_dict(result)

    @log
    async def rotor_session_feedback_radio_started(
        self,
        radio_session_id: str,
        batch_id: Optional[str] = None,
        from_: Optional[str] = None,
        timestamp: TimestampType = None,
        **kwargs: Any,
    ) -> bool:
        """Отправка обратной связи сессии радио: начало прослушивания радио.

        Args:
            radio_session_id (:obj:`str`): Уникальный идентификатор сессии.
            batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
            from_ (:obj:`str`, optional): Откуда начато воспроизведение.
            timestamp (:obj:`str` | :obj:`float` | :obj:`int`, optional): Время события в формате ISO 8601.
                По умолчанию текущее.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        event = SessionEvent('radioStarted', timestamp or utc_now_iso())

        return await self.rotor_session_feedback(radio_session_id, event, batch_id, from_, **kwargs)

    @log
    async def rotor_session_feedback_track_started(
        self,
        radio_session_id: str,
        track_id: Union[str, int],
        batch_id: Optional[str] = None,
        timestamp: TimestampType = None,
        **kwargs: Any,
    ) -> bool:
        """Отправка обратной связи сессии радио: начало воспроизведения трека.

        Args:
            radio_session_id (:obj:`str`): Уникальный идентификатор сессии.
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека (`id` или `id:album_id`).
            batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
            timestamp (:obj:`str` | :obj:`float` | :obj:`int`, optional): Время события в формате ISO 8601.
                По умолчанию текущее.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        event = SessionEvent('trackStarted', timestamp or utc_now_iso(), track_id=str(track_id))

        return await self.rotor_session_feedback(radio_session_id, event, batch_id, **kwargs)

    @log
    async def rotor_session_feedback_track_finished(
        self,
        radio_session_id: str,
        track_id: Union[str, int],
        total_played_seconds: Union[int, float],
        batch_id: Optional[str] = None,
        timestamp: TimestampType = None,
        **kwargs: Any,
    ) -> bool:
        """Отправка обратной связи сессии радио: окончание воспроизведения трека.

        Args:
            radio_session_id (:obj:`str`): Уникальный идентификатор сессии.
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека (`id` или `id:album_id`).
            total_played_seconds (:obj:`int` | :obj:`float`): Сколько секунд трека было проиграно.
            batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
            timestamp (:obj:`str` | :obj:`float` | :obj:`int`, optional): Время события в формате ISO 8601.
                По умолчанию текущее.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        event = SessionEvent(
            'trackFinished',
            timestamp or utc_now_iso(),
            track_id=str(track_id),
            total_played_seconds=total_played_seconds,
        )

        return await self.rotor_session_feedback(radio_session_id, event, batch_id, **kwargs)

    @log
    async def rotor_session_feedback_skip(
        self,
        radio_session_id: str,
        track_id: Union[str, int],
        total_played_seconds: Union[int, float],
        batch_id: Optional[str] = None,
        timestamp: TimestampType = None,
        **kwargs: Any,
    ) -> bool:
        """Отправка обратной связи сессии радио: пропуск трека.

        Args:
            radio_session_id (:obj:`str`): Уникальный идентификатор сессии.
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека (`id` или `id:album_id`).
            total_played_seconds (:obj:`int` | :obj:`float`): Сколько секунд трека было проиграно до пропуска.
            batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
            timestamp (:obj:`str` | :obj:`float` | :obj:`int`, optional): Время события в формате ISO 8601.
                По умолчанию текущее.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        event = SessionEvent(
            'skip', timestamp or utc_now_iso(), track_id=str(track_id), total_played_seconds=total_played_seconds
        )

        return await self.rotor_session_feedback(radio_session_id, event, batch_id, **kwargs)

    @log
    async def rotor_session_feedbacks(
        self, radio_session_id: str, feedbacks: List[SessionFeedback], **kwargs: Any
    ) -> bool:
        """Отправка нескольких событий обратной связи сессии радио одним запросом.

        Args:
            radio_session_id (:obj:`str`): Уникальный идентификатор сессии.
            feedbacks (:obj:`list` из :obj:`yandex_music.SessionFeedback`): Обратная связь.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/session/{radio_session_id}/feedbacks'

        body = {'feedbacks': [feedback.to_dict(for_request=True) for feedback in feedbacks]}

        result = await self._request.post(url, json=body, **kwargs)

        return is_dict(result)

    @log
    async def rotor_sessions_feedbacks(self, sessions: List[SessionFeedbacks], **kwargs: Any) -> bool:
        """Отправка обратной связи сразу по нескольким сессиям радио.

        Args:
            sessions (:obj:`list` из :obj:`yandex_music.SessionFeedbacks`): Обратная связь по сессиям.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/sessions/feedbacks'

        body = {'sessions': [session.to_dict(for_request=True) for session in sessions]}

        result = await self._request.post(url, json=body, **kwargs)

        return is_dict(result)

    @log
    async def rotor_combined_session_new(
        self,
        supported_types: Optional[List[str]] = None,
        queue: Optional[List[CombinedSessionQueueItem]] = None,
        child: Optional[bool] = None,
        allow_explicit: Optional[bool] = None,
        **kwargs: Any,
    ) -> Optional[CombinedSession]:
        """Создание комбинированной сессии радио (треки и клипы).

        Note:
            Известные значения `supported_types`: `CLIP`, `TRACK`.

        Args:
            supported_types (:obj:`list` из :obj:`str`, optional): Типы элементов, которые поддерживает клиент.
            queue (:obj:`list` из :obj:`yandex_music.CombinedSessionQueueItem`, optional): Уже полученные элементы.
            child (:obj:`bool`, optional): Детский режим.
            allow_explicit (:obj:`bool`, optional): Разрешить ли контент с ненормативной лексикой.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.CombinedSession` | :obj:`None`: Комбинированная сессия или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/combined/session/new'

        body: Dict[str, Any] = {
            'supportedTypes': supported_types,
            'queue': [item.to_dict(for_request=True) for item in queue] if queue is not None else None,
            'child': child,
            'allowExplicit': allow_explicit,
        }
        body = {key: value for key, value in body.items() if value is not None}

        result = await self._request.post(url, json=body, **kwargs)

        return CombinedSession.de_json(result, self)

    @log
    async def rotor_combined_session_next(
        self, session_id: str, queue: Optional[List[CombinedSessionQueueItem]] = None, **kwargs: Any
    ) -> Optional[CombinedSession]:
        """Получение следующих элементов комбинированной сессии радио.

        Args:
            session_id (:obj:`str`): Уникальный идентификатор комбинированной сессии.
            queue (:obj:`list` из :obj:`yandex_music.CombinedSessionQueueItem`, optional): Уже полученные элементы.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.CombinedSession` | :obj:`None`: Следующие элементы сессии или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/combined/session/{session_id}/next'

        body = {'queue': [item.to_dict(for_request=True) for item in queue or []]}

        result = await self._request.post(url, json=body, **kwargs)

        return CombinedSession.de_json(result, self)

    @log
    async def rotor_combined_session_landing(
        self,
        supported_types: Optional[List[str]] = None,
        child: Optional[bool] = None,
        allow_explicit: Optional[bool] = None,
        **kwargs: Any,
    ) -> Optional[CombinedSessionLanding]:
        """Получение витрины комбинированной сессии радио (например, «Время клипов»).

        Note:
            Известные значения `supported_types`: `CLIP`, `TRACK`.

        Args:
            supported_types (:obj:`list` из :obj:`str`, optional): Типы элементов, которые поддерживает клиент.
            child (:obj:`bool`, optional): Детский режим.
            allow_explicit (:obj:`bool`, optional): Разрешить ли контент с ненормативной лексикой.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.CombinedSessionLanding` | :obj:`None`: Витрина или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/rotor/combined/session/landing'

        body: Dict[str, Any] = {
            'supportedTypes': supported_types,
            'child': child,
            'allowExplicit': allow_explicit,
        }
        body = {key: value for key, value in body.items() if value is not None}

        result = await self._request.post(url, json=body, **kwargs)

        return CombinedSessionLanding.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`rotor_session_new`
    rotorSessionNew = rotor_session_new
    #: Псевдоним для :attr:`rotor_session_clone`
    rotorSessionClone = rotor_session_clone
    #: Псевдоним для :attr:`rotor_session_tracks`
    rotorSessionTracks = rotor_session_tracks
    #: Псевдоним для :attr:`rotor_session_feedback`
    rotorSessionFeedback = rotor_session_feedback
    #: Псевдоним для :attr:`rotor_session_feedback_radio_started`
    rotorSessionFeedbackRadioStarted = rotor_session_feedback_radio_started
    #: Псевдоним для :attr:`rotor_session_feedback_track_started`
    rotorSessionFeedbackTrackStarted = rotor_session_feedback_track_started
    #: Псевдоним для :attr:`rotor_session_feedback_track_finished`
    rotorSessionFeedbackTrackFinished = rotor_session_feedback_track_finished
    #: Псевдоним для :attr:`rotor_session_feedback_skip`
    rotorSessionFeedbackSkip = rotor_session_feedback_skip
    #: Псевдоним для :attr:`rotor_session_feedbacks`
    rotorSessionFeedbacks = rotor_session_feedbacks
    #: Псевдоним для :attr:`rotor_sessions_feedbacks`
    rotorSessionsFeedbacks = rotor_sessions_feedbacks
    #: Псевдоним для :attr:`rotor_combined_session_new`
    rotorCombinedSessionNew = rotor_combined_session_new
    #: Псевдоним для :attr:`rotor_combined_session_next`
    rotorCombinedSessionNext = rotor_combined_session_next
    #: Псевдоним для :attr:`rotor_combined_session_landing`
    rotorCombinedSessionLanding = rotor_combined_session_landing
