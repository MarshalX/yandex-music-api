from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yandex_music.utils.captcha_response import CaptchaResponse


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


class InvalidBitrate(YandexMusicError):
    """Класс исключения, вызываемого при попытке загрузки трека
    с недоступным битрейтом.
    """


class Captcha(YandexMusicError):
    """Базовый класс, представляющий исключение связанное с капчей.

    Attributes:
        captcha (:obj:`yandex_music.utils.captcha_response.CaptchaResponse`): Капча.

    Args:
        msg (:obj:`str`): Сообщение с ошибкой.
        captcha (:obj:`yandex_music.utils.captcha_response.CaptchaResponse`): Капча.
    """

    def __init__(self, msg: str, captcha: 'CaptchaResponse', *args, **kwargs):
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
    """Класс исключения, вызываемый в случае отправки неправильного запроса.
    """
    pass


class TimedOut(NetworkError):
    """Класс исключения, вызываемого для случаев истечения времени ожидания.
    """

    def __init__(self):
        super().__init__('Timed out')
