from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class PersonalPlaylistsData(YandexMusicObject):
    def __init__(self,
                 is_wizard_passed: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.is_wizard_passed = is_wizard_passed

        self.client = client
        self._id_attrs = (self.is_wizard_passed,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PersonalPlaylistsData']:
        if not data:
            return None

        data = super(PersonalPlaylistsData, cls).de_json(data, client)

        return cls(client=client, **data)
