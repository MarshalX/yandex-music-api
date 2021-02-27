from typing import TYPE_CHECKING


class YandexMusicError(Exception):
    """Базовый класс, представляющий исключения общего характера. """


class Unauthorized(YandexMusicError):
    """Класс исключения, вызываемого для случаев ошибок
    аутентификации и авторизации.
    """


class InvalidBitrate(YandexMusicError):
    """Класс исключения, вызываемого при попытке загрузки трека
    с недоступным битрейтом.
    """


class Captcha(YandexMusicError):
    """Базовый класс, представляющий исключение связанное с капчей.

    Attributes:
        captcha_image_url (:obj:`str` | :obj:`None`): Ссылка на изображение с капчей.

    Args:
        msg (:obj:`str`): Сообщение с ошибкой.
        captcha_image_url (:obj:`str`, optional): Ссылка на изображение с капчей.
    """

    def __init__(self, msg: str, captcha_image_url: str = None, *args):
        self.captcha_image_url = captcha_image_url
        super().__init__(msg, *args)


class CaptchaRequired(Captcha):
    """Класс исключения, вызываемый в случае необходимости ввода проверочного кода."""


class CaptchaNotShown(Captcha):
    """Класс исключения, вызываемый в случае когда капча была получена, но изображение не было загружено.

    Notes:
        Будет вызвано если не сделать запрос на `captcha_image_url` полученный в `CaptchaRequired`. Получив данное
        исключение можно выполнить запрос еще раз для получения новой капчи.

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
