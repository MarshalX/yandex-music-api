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


class Captcha(YandexMusicError):
    """Базовый класс, представляющий исключение связанное с капчей.

    Attributes:
        captcha (:obj:`yandex_music.utils.captcha_response.CaptchaResponse`): Объект класса
            :class:`yandex_music.utils.captcha_response.CaptchaResponse` представляющий капчу.

    Args:
        msg (:obj:`str`): Сообщение с ошибкой.
        captcha (:obj:`yandex_music.utils.captcha_response.CaptchaResponse`): Объект класса
            :class:`yandex_music.utils.captcha_response.CaptchaResponse` представляющий капчу.
    """

    def __init__(self, msg, captcha, *args, **kwargs):
        self.captcha = captcha
        super().__init__(msg, *args, **kwargs)


class CaptchaRequired(Captcha):
    """Класс исключения, вызываемый в случае необходимости ввода проверочного кода.
    """

    pass


class CaptchaWrong(Captcha):
    """Класс исключения, вызываемый в случае неправильного ввода капчи.
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
        super().__init__('Timed out')
