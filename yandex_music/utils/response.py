from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, InvocationInfo


@model
class Response(YandexMusicObject):
    """Класс, представляющий ответ API.

    Note:
        У ответа сервера два варианта возврата данных. Через корень (без вложенности, на уровне `invocation_info`)
        используется от силы пару раз. И в поле `result`. Второй считается основным.

        В `data` лежит копия всего ответа.

    Attributes:
        data (:obj:`dict`): Ответ на запрос. Используется тогда, когда отсутствует `result`.
        invocation_info (:obj:`yandex_music.InvocationInfo`, optional): Информация о запросе.
        result (:obj:`dict`, optional): Ответ на запрос (секция с результатом).
        error (:obj:`str`, optional): Код ошибки.
        error_description (:obj:`str`, optional): Описание ошибки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    data: dict
    invocation_info: Optional['InvocationInfo'] = None
    result: dict = None
    error: str = None
    error_description: str = None
    client: Optional['Client'] = None

    def get_error(self) -> str:
        """:obj:`str`: Код ошибки вместе с описанием"""
        return f'{self.error} {self.error_description if self.error_description else ""}'

    def get_result(self) -> dict:
        """:obj:`dict`: Результат выполнения запроса. Данный для распаковки."""
        return self.data if self.result is None else self.result

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
