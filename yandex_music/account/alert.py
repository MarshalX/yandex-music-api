from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import AlertButton, ClientType, JSONType


@model
class Alert(YandexMusicModel):
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
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.alert_id,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Alert']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Alert`: Сообщение о статусе подписки.
        """
        if not cls.is_dict_model_data(data):
            return None

        from yandex_music import AlertButton

        cls_data = cls.cleanup_data(data, client)
        cls_data['button'] = AlertButton.de_json(data.get('button'), client)

        return cls(client=client, **cls_data)  # type: ignore
