from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, AlertButton


@model
class Alert(YandexMusicObject):
    """Класс, представляющий блок с предупреждением.

    Note:
        Данные предупреждения, скорее всего, только обкатываются. У них нет ID, вместо этого `xxx`, а еще присутствуют
        слова "тест" в тексте.

        Используют как предупреждение о конце подписки, так и о раздаче подарков.

    Attributes:
        alert_id (:obj:`str`): Уникальный идентификатор.
        text (:obj:`str`): Текст предупреждения.
        bg_color (:obj:`str`): Цвет заднего фона.
        text_color (:obj:`str`): Цвет текста.
        alert_type (:obj:`str`): Тип предупреждения.
        button (:obj:`yandex_music.AlertButton`): Кнопка с ссылкой.
        close_button (:obj:`bool`): Наличие кнопки "Закрыть".
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    alert_id: str
    text: str
    bg_color: str
    text_color: str
    alert_type: str
    button: 'AlertButton'
    close_button: bool
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.alert_id,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Alert']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Alert`: Сообщение о статусе подписки.
        """
        if not data:
            return None

        from yandex_music import AlertButton

        data = super(Alert, cls).de_json(data, client)
        data['button'] = AlertButton.de_json(data.get('button'), client)

        return cls(client=client, **data)
