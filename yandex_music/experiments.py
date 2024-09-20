from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Experiments(YandexMusicModel):
    """Класс, представляющий какие-то свистелки и перделки, флажки, режимы экспериментальных функций.

    Attributes:
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
        название_эксперимента (:obj:`str`): Содержит режим или состояние, или функцию, или ещё что угодно.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Собственно тут и передаются все эти свистелки.
    """

    def __init__(self, client: Optional['Client'] = None, **kwargs) -> None:
        self.__dict__.update(kwargs)

        self.client = client
