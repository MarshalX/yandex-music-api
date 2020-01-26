from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Playlist


class GeneratedPlaylist(YandexMusicObject):
    def __init__(self,
                 type_: str,
                 ready: bool,
                 notify: bool,
                 data: Optional['Playlist'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.ready = ready
        self.notify = notify
        self.data = data

        self.client = client
        self._id_attrs = (self.type, self.ready, self.notify, self.data)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['GeneratedPlaylist']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.GeneratedPlaylist`: Объект класса :class:`yandex_music.GeneratedPlaylist`.
        """
        if not data:
            return None

        data = super(GeneratedPlaylist, cls).de_json(data, client)
        from yandex_music import Playlist
        data['data'] = Playlist.de_json(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['GeneratedPlaylist']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.GeneratedPlaylist`: Список объектов класса
            :class:`yandex_music.GeneratedPlaylist`.
        """
        if not data:
            return []

        generated_playlists = list()
        for generated_playlist in data:
            generated_playlists.append(cls.de_json(generated_playlist, client))

        return generated_playlists
