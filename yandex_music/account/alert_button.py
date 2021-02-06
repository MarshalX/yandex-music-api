from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class AlertButton(YandexMusicObject):
    """Класс, представляющий кнопку в предупреждении.

    Attributes:
        text (:obj:`str`): Текст кнопки.
        bg_color (:obj:`str`): Цвет заднего фона.
        text_color (:obj:`str`): Цвет текста.
        uri (:obj:`str`): Ссылка куда ведёт кнопка.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        text (:obj:`str`): Текст кнопки.
        bg_color (:obj:`str`): Цвет заднего фона.
        text_color (:obj:`str`): Цвет текста.
        uri (:obj:`str`): Ссылка куда ведёт кнопка.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self, text: str, bg_color: str, text_color: str, uri: str, client: Optional['Client'] = None, **kwargs
    ) -> None:
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.uri = uri

        self.client = client
        self._id_attrs = (self.text, self.uri)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['AlertButton']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.AlertButton`: Кнопка в статусе о подписки.
        """
        if not data:
            return None

        data = super(AlertButton, cls).de_json(data, client)

        return cls(client=client, **data)
