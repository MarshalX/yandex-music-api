from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class CaptchaResponse(YandexMusicObject):
    """Класс, представляющий ответ сервера с запросом на ввод капчи.

    Attributes:
        x_captcha_url (:obj:`str`): Ссылка на изображение с капчей.
        x_captcha_key (:obj:`str`): Уникальный ключ капчи.
        error_description (:obj:`str`): Описание ошибки.
        error (:obj:`str`): Код ошибки.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        x_captcha_url (:obj:`str`): Ссылка на изображение с капчей.
        x_captcha_key (:obj:`str`): Уникальный ключ капчи.
        error_description (:obj:`str`): Описание ошибки.
        error (:obj:`str`): Код ошибки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 x_captcha_url,
                 x_captcha_key,
                 error_description,
                 error,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.x_captcha_url = x_captcha_url
        self.x_captcha_key = x_captcha_key
        self.error_description = error_description
        self.error = error

        self.client = client
        self._id_attrs = (self.x_captcha_key, self.x_captcha_url)

    def download(self, filename=None):
        """Загрузка изображения с капчей.

        Args:
            filename (:obj:`str`, optional): Путь и(или) название файла вместе с расширением. По умолчанию ключ
                капчи и расширение `.gif`.
        """
        if not filename:
            filename = f'{self.x_captcha_key}.gif'

        self.client.request.download(self.x_captcha_url, filename)

    @classmethod
    def de_json(cls, data: dict, client: 'Client'):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.utils.captcha_response.CaptchaResponse`: Ответ сервера с запросом на ввод капчи.
        """
        if not data:
            return None

        data = super(CaptchaResponse, cls).de_json(data, client)

        return cls(client=client, **data)
