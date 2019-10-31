class YandexMusicError(Exception):
    pass


class InvalidToken(YandexMusicError):
    pass


class Unauthorized(YandexMusicError):
    pass


class NetworkError(YandexMusicError):
    """Базовый класс исключений, вызываемых для ошибок, связанных с
    запросами к серверу.
    """

    pass


class BadRequest(NetworkError):
    pass


class TimedOut(NetworkError):
    def __init__(self):
        super(TimedOut, self).__init__('Timed out')
