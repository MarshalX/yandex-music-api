from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, InvocationInfo


class Response(YandexMusicObject):
    """Класс, представляющий ответ API.

    Note:
        У ответа сервера два варианта возврата данных. Через корень (без вложенности, на уровне `invocation_info`)
        используется от силы пару раз. И в поле `result`. Второй считается основным.

        В `data` лежит копия всего ответа.

    Attributes:
        data (:obj:`dict`): Ответ на запрос. Используется тогда, когда отсутствует `result`.
        invocation_info (:obj:`yandex_music.InvocationInfo` | :obj:`None`): Информация о запросе.
        result (:obj:`dict`): Ответ на запрос (секция с результатом).
        error (:obj:`str`): Код ошибки.
        error_description (:obj:`str`): Описание ошибки.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        data (:obj:`dict`): Ответ на запрос. Используется тогда, когда отсутствует `result`.
        invocation_info (:obj:`yandex_music.InvocationInfo`, optional): Информация о запросе.
        result (:obj:`dict`, optional): Ответ на запрос (секция с результатом).
        error (:obj:`str`, optional): Код ошибки.
        error_description (:obj:`str`, optional): Описание ошибки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 data: dict,
                 invocation_info: Optional['InvocationInfo'] = None,
                 result: dict = None,
                 error: str = None,
                 error_description: str = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.data = data
        self.invocation_info = invocation_info
        self._result = result
        self._error = error
        self.error_description = error_description

        self.client = client

    @property
    def error(self) -> str:
        """:obj:`str`: Код ошибки вместе с описанием"""
        return f'{self._error} {self.error_description if self.error_description else ""}'

    @property
    def result(self) -> dict:
        """:obj:`dict`: Результат выполнения запроса. Данный для распаковки."""
        return self.data if self._result is None else self._result

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Response']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.utils.response.Response`: Ответ API.
        """
        if not data:
            return None

        data = super(Response, cls).de_json(data, client)
        data['data'] = data.copy()
        from yandex_music import InvocationInfo
        data['invocation_info'] = InvocationInfo.de_json(data.get('invocation_info'), client)

        return cls(client=client, **data)
