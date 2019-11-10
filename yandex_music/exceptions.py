class YandexMusicError(Exception):
    """Базовый класс, представляющий исключения общего характера. """

    pass


class InvalidToken(YandexMusicError):
    """Класс исключения, вызываемого для случаев недействительного
    или неверного токена аутентификации.
    """

    pass


class Unauthorized(YandexMusicError):
    """Класс исключения, вызываемого для случаев ошибок
    аутентификации и авторизации.
    """

    pass


class NetworkError(YandexMusicError):
    """Базовый класс исключений, вызываемых для ошибок, связанных с
    запросами к серверу.
    """

    pass


class BadRequest(NetworkError):
    pass


class TimedOut(NetworkError):
    """Класс исключения, вызываемого для случаев истечения времени ожидания.
    """

    def __init__(self):
        super(TimedOut, self).__init__('Timed out')
