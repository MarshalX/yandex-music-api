class YandexMusicError(Exception):
    """Базовый класс, представляющий исключения общего характера."""


class Unauthorized(YandexMusicError):
    """Класс исключения, вызываемого для случаев ошибок
    аутентификации и авторизации.
    """


class InvalidBitrate(YandexMusicError):
    """Класс исключения, вызываемого при попытке загрузки трека
    с недоступным битрейтом.
    """


class NetworkError(YandexMusicError):
    """Базовый класс исключений, вызываемых для ошибок, связанных с
    запросами к серверу.
    """


class BadRequest(NetworkError):
    """Класс исключения, вызываемый в случае отправки неправильного запроса."""


class TimedOut(NetworkError):
    """Класс исключения, вызываемого для случаев истечения времени ожидания."""

    def __init__(self):
        super().__init__('Timed out')
