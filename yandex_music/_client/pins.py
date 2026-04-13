#############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/pins.py. DON'T EDIT IT BY HANDS #
#############################################################################################

from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import Pin
from yandex_music._client import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class PinsMixin(ClientBase):
    """Миксин для методов, связанных с закреплёнными элементами."""

    _request: 'Request'

    @log
    def pins(self, *args: Any, **kwargs: Any) -> List[Pin]:
        """Получение списка закреплённых элементов.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Pin`: Список закреплённых элементов.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pins'

        result = self._request.get(url, *args, **kwargs)

        if isinstance(result, dict):
            return list(Pin.de_list(result.get('pins'), self))

        return []

    @log
    def pin_album(self, album_id: Union[str, int], **kwargs: Any) -> Optional[Pin]:
        """Закрепление альбома.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Pin`: Закреплённый элемент.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pin/album'

        result = self._request.put(url, json={'id': album_id}, **kwargs)

        return Pin.de_json(result, self)

    @log
    def unpin_album(self, album_id: Union[str, int], **kwargs: Any) -> bool:
        """Открепление альбома.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pin/album'

        result = self._request.delete(url, json={'id': album_id}, **kwargs)

        return result == 'ok'

    @log
    def pin_artist(self, artist_id: Union[str, int], **kwargs: Any) -> Optional[Pin]:
        """Закрепление артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Pin`: Закреплённый элемент.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pin/artist'

        result = self._request.put(url, json={'id': artist_id}, **kwargs)

        return Pin.de_json(result, self)

    @log
    def unpin_artist(self, artist_id: Union[str, int], **kwargs: Any) -> bool:
        """Открепление артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pin/artist'

        result = self._request.delete(url, json={'id': artist_id}, **kwargs)

        return result == 'ok'

    @log
    def pin_playlist(self, uid: Union[str, int], kind: Union[str, int], **kwargs: Any) -> Optional[Pin]:
        """Закрепление плейлиста.

        Args:
            uid (:obj:`str` | :obj:`int`): Уникальный идентификатор владельца плейлиста.
            kind (:obj:`str` | :obj:`int`): Номер плейлиста.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Pin`: Закреплённый элемент.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pin/playlist'

        result = self._request.put(url, json={'uid': uid, 'kind': kind}, **kwargs)

        return Pin.de_json(result, self)

    @log
    def unpin_playlist(self, uid: Union[str, int], kind: Union[str, int], **kwargs: Any) -> bool:
        """Открепление плейлиста.

        Args:
            uid (:obj:`str` | :obj:`int`): Уникальный идентификатор владельца плейлиста.
            kind (:obj:`str` | :obj:`int`): Номер плейлиста.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pin/playlist'

        result = self._request.delete(url, json={'uid': uid, 'kind': kind}, **kwargs)

        return result == 'ok'

    @log
    def pin_wave(self, seeds: str, **kwargs: Any) -> Optional[Pin]:
        """Закрепление волны.

        Args:
            seeds (:obj:`str`): Идентификатор волны (например, "artist:12345").
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Pin`: Закреплённый элемент.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pin/wave'

        result = self._request.put(url, json={'seeds': seeds}, **kwargs)

        return Pin.de_json(result, self)

    @log
    def unpin_wave(self, seeds: str, **kwargs: Any) -> bool:
        """Открепление волны.

        Args:
            seeds (:obj:`str`): Идентификатор волны.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/pin/wave'

        result = self._request.delete(url, json={'seeds': seeds}, **kwargs)

        return result == 'ok'
