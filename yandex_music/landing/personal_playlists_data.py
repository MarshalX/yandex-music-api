from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class PersonalPlaylistsData(YandexMusicObject):
    """Класс, представляющий дополнительную информацию о персональном плейлисте.

    Attributes:
        is_wizard_passed (:obj:`bool`): TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        is_wizard_passed (:obj:`bool`): TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 is_wizard_passed: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.is_wizard_passed = is_wizard_passed

        self.client = client
        self._id_attrs = (self.is_wizard_passed,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PersonalPlaylistsData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PersonalPlaylistsData`: Дополнительная информация о персональном плейлисте.
        """
        if not data:
            return None

        data = super(PersonalPlaylistsData, cls).de_json(data, client)

        return cls(client=client, **data)
