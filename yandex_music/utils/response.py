from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Response(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 data,
                 invocation_info=None,
                 result=None,
                 error=None,
                 error_description=None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.data = data
        self.invocation_info = invocation_info
        self._result = result
        self._error = error
        self.error_description = error_description

        self.client = client

    @property
    def error(self):
        return f'{self._error} {self.error_description if self.error_description else ""}'

    @property
    def result(self):
        return self.data if self._result is None else self._result

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Response']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.utils.response.Response`: Объект класса :class:`yandex_music.utils.response.Response`.
        """
        if not data:
            return None

        data = super(Response, cls).de_json(data, client)
        data['data'] = data.copy()
        from yandex_music import InvocationInfo
        data['invocation_info'] = InvocationInfo.de_json(data.get('invocation_info'), client)

        return cls(client=client, **data)
