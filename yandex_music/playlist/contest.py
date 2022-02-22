from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Contest(YandexMusicObject):
    """Класс, представляющий контест TODO.

    Note:
        Известные значения поля `status`: `editing`, `withdrew-moderator`.

    Attributes:
        contest_id (:obj:`str`): Уникальный идентификатор.
        status (:obj:`str`): Статус.
        can_edit (:obj:`bool`): Разрешено ли редактирование.
        sent (:obj:`str`, optional): Дата отправки.
        withdrawn (:obj:`str`, optional): Дата вывода (окончания).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    contest_id: str
    status: str
    can_edit: bool
    sent: Optional[str] = None
    withdrawn: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.contest_id, self.status)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Contest']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Contest`: Контест.
        """
        if not data:
            return None

        data = super(Contest, cls).de_json(data, client)

        return cls(client=client, **data)
