"""Модели Ynison Redirect."""

from dataclasses import dataclass

import betterproto


@dataclass
class RedirectResponse(betterproto.Message):
    """Класс, представляющий ответ сервиса редиректа Ynison.

    Attributes:
        host (:obj:`str`): Целевой хост для подключения к Ynison.
        redirect_ticket (:obj:`str`): Билет, который нужно передать в заголовке при подключении
            к Ynison. Защищает от DDoS-атак на отдельный хост. Проверяется до аутентификации в BB.
        session_id (:obj:`int`): Уникальный идентификатор сессии. Используется для логирования и отладки.
            Для удобства отладки стоит с ним же прийти в Ynison впоследствии.
        keep_alive_params (:obj:`yandex_music.ynison.models.ynison_redirect.KeepAliveParams`):
            Настройки keep-alive при подключении к Ynison.
    """

    host: str = betterproto.string_field(1)
    redirect_ticket: str = betterproto.string_field(2)
    session_id: int = betterproto.int64_field(3)
    keep_alive_params: 'KeepAliveParams' = betterproto.message_field(4)


@dataclass
class KeepAliveParams(betterproto.Message):
    """Класс, представляющий параметры keep-alive для подключения к Ynison.

    Attributes:
        keep_alive_time_seconds (:obj:`int`): Интервал отправки ping-фреймов, в секундах.
        keep_alive_timeout_seconds (:obj:`int`): Таймаут ожидания pong-ответа, в секундах.
    """

    keep_alive_time_seconds: int = betterproto.int32_field(1)
    keep_alive_timeout_seconds: int = betterproto.int32_field(2)
