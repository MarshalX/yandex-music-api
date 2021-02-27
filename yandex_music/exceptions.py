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
        track_id (:obj:`str`): Идентификатора сессии аутентификации.
        captcha_image_url (:obj:`str` | :obj:`None`): Ссылка на изображение с капчей.

    Args:
        msg (:obj:`str`): Сообщение с ошибкой.
        track_id (:obj:`str`, optional): Идентификатора сессии аутентификации.
        captcha_image_url (:obj:`str`, optional): Ссылка на изображение с капчей.
    """

    def __init__(self, msg: str, track_id: str = None, captcha_image_url: str = None, *args):
        super().__init__(msg, *args)
        self.track_id = track_id
        self.captcha_image_url = captcha_image_url


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
