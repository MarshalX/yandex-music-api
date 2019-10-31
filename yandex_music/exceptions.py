class YandexMusicError(Exception):
    pass


class InvalidToken(YandexMusicError):
    pass


class Unauthorized(YandexMusicError):
    pass


class NetworkError(YandexMusicError):
    pass


class BadRequest(NetworkError):
    """Класс исключения, вызываемого в случаях ошибок
    в запросе клиента к серверу.
    """

    pass


class TimedOut(NetworkError):
    def __init__(self):
        super(TimedOut, self).__init__('Timed out')
