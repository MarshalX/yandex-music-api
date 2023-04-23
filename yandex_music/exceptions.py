class YandexMusicError(Exception):
    """Базовый класс, представляющий исключения общего характера."""


class UnauthorizedError(YandexMusicError):
    """Класс исключения, вызываемого для случаев ошибок
    аутентификации и авторизации.
    """


# TODO (MarshalX) На самом деле поиск еще происходит по кодеку
#  https://github.com/MarshalX/yandex-music-api/issues/552
class InvalidBitrateError(YandexMusicError):
    """Класс исключения, вызываемого при попытке загрузки трека
    с недоступным битрейтом.
    """


class NetworkError(YandexMusicError):
    """Базовый класс исключений, вызываемых для ошибок, связанных с
    запросами к серверу.
    """


class BadRequestError(NetworkError):
    """Класс исключения, вызываемый в случае отправки неправильного запроса."""


class NotFoundError(NetworkError):
    """Класс исключения, вызываемый в случае ответа от сервера со статус кодом 404."""


# TimeoutError builtin. Пока не знаю хотим ли использовать его для синхронной и asyncio.TimeoutError для асинхронной
class TimedOutError(NetworkError):
    """Класс исключения, вызываемого для случаев истечения времени ожидания."""

    def __init__(self):
        super().__init__('Timed out')
