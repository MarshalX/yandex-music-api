"""Исключения."""

import typing


class YandexMusicError(Exception):
    """Базовый класс, представляющий исключения общего характера."""


class UnauthorizedError(YandexMusicError):
    """Класс исключения, вызываемого для случаев ошибок аутентификации и авторизации."""


# TODO (MarshalX) На самом деле поиск еще происходит по кодеку
#  https://github.com/MarshalX/yandex-music-api/issues/552
class InvalidBitrateError(YandexMusicError):
    """Класс исключения, вызываемого при попытке загрузки трека с недоступным битрейтом."""


class IdMissingError(YandexMusicError):
    """Класс исключения, вызываемого при попытке использования отсутствующего ID."""


class NetworkError(YandexMusicError):
    """Базовый класс исключений, вызываемых для ошибок, связанных с запросами к серверу."""


class BadRequestError(NetworkError):
    """Класс исключения, вызываемый в случае отправки неправильного запроса."""


class NotFoundError(NetworkError):
    """Класс исключения, вызываемый в случае ответа от сервера со статус кодом 404."""


# TimeoutError builtin. Пока не знаю хотим ли использовать его для синхронной и asyncio.TimeoutError для асинхронной
class TimedOutError(NetworkError):
    """Класс исключения, вызываемого для случаев истечения времени ожидания."""

    def __init__(self) -> None:
        super().__init__('Timed out')


class DeviceAuthError(YandexMusicError):
    """Класс исключения, вызываемого при ошибках OAuth Device Flow (кроме `authorization_pending`)."""


class YnisonError(YandexMusicError):
    """Базовый класс исключений, вызываемых для ошибок, связанных с Ynison."""


class YnisonTimeoutError(YnisonError):
    """Класс исключения, вызываемого при истечении времени ожидания ответа от Ynison."""


class YnisonConnectionClosedError(YnisonError):
    """Класс исключения, вызываемого при отправке в закрытое или потерянное соединение Ynison."""


class YnisonNoActiveDeviceError(YnisonError):
    """Класс исключения, вызываемого, когда для команды нет активного (играющего) устройства."""


class YnisonQueueBoundaryError(YnisonError):
    """Класс исключения, вызываемого при попытке переключить трек за пределы очереди."""


class YnisonServerError(YnisonError):
    """Класс исключения, представляющего ошибку, присланную сервером Ynison.

    Attributes:
        message (:obj:`str`): Текст ошибки от сервера.
        grpc_code (:obj:`int` | :obj:`None`): gRPC-код ошибки.
        http_code (:obj:`int` | :obj:`None`): HTTP-код ошибки.
        error_code (:obj:`str` | :obj:`None`): Внутренний код ошибки Ynison (`ynison-error-code`).
        backoff_ms (:obj:`list` из :obj:`int`): Рекомендуемая сервером лестница задержек
            перед повторными подключениями, в миллисекундах.
        go_away_seconds (:obj:`int` | :obj:`None`): Время, в течение которого сервер просит
            не переподключаться, в секундах.
    """

    def __init__(
        self,
        message: str,
        grpc_code: typing.Optional[int] = None,
        http_code: typing.Optional[int] = None,
        error_code: typing.Optional[str] = None,
        backoff_ms: typing.Optional[typing.List[int]] = None,
        go_away_seconds: typing.Optional[int] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.grpc_code = grpc_code
        self.http_code = http_code
        self.error_code = error_code
        self.backoff_ms = backoff_ms or []
        self.go_away_seconds = go_away_seconds


class YnisonUnauthorizedError(YnisonServerError):
    """Класс исключения, вызываемого при ошибке аутентификации в Ynison (неверный или истёкший токен)."""


class YnisonDeviceDisplacedError(YnisonServerError):
    """Класс исключения, вызываемого, когда соединение вытеснено другим клиентом с тем же `device_id`.

    Сервер закрывает старое соединение, если подключается новое с тем же идентификатором
    устройства. Один `device_id` может использоваться только одним живым подключением.
    """
