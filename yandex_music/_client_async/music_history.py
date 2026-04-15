from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from yandex_music import MusicHistory, MusicHistoryItems
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


def _make_item(type_: str, item_id: Dict[str, Any]) -> Dict[str, Any]:
    return {'type': type_, 'data': {'itemId': item_id}}


def _build_history_items(
    track_ids: Optional[List[Tuple[Union[str, int], Union[str, int]]]] = None,
    album_ids: Optional[List[Union[str, int]]] = None,
    artist_ids: Optional[List[Union[str, int]]] = None,
    playlist_ids: Optional[List[Tuple[Union[str, int], Union[str, int]]]] = None,
    wave_seeds: Optional[List[List[str]]] = None,
) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for track_id, album_id in track_ids or []:
        items.append(_make_item('track', {'trackId': str(track_id), 'albumId': str(album_id)}))
    for album_id in album_ids or []:
        items.append(_make_item('album', {'id': str(album_id)}))
    for artist_id in artist_ids or []:
        items.append(_make_item('artist', {'id': str(artist_id)}))
    for uid, kind in playlist_ids or []:
        items.append(_make_item('playlist', {'uid': int(uid), 'kind': int(kind)}))
    for seeds in wave_seeds or []:
        items.append(_make_item('wave', {'seeds': seeds}))
    return items


class MusicHistoryMixin(ClientBase):
    """Миксин для методов, связанных с историей прослушивания."""

    _request: 'Request'

    @log
    async def music_history(
        self,
        full_models_count: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[MusicHistory]:
        """Получение истории прослушивания.

        Args:
            full_models_count (:obj:`int`, optional): Количество полных моделей для возврата.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.MusicHistory` | :obj:`None`: История прослушивания или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/music-history'

        params = {
            'fullModelsCount': full_models_count,
        }

        result = await self._request.get(url, params, *args, **kwargs)

        return MusicHistory.de_json(result, self)

    @log
    async def music_history_items(
        self,
        track_ids: Optional[List[Tuple[Union[str, int], Union[str, int]]]] = None,
        album_ids: Optional[List[Union[str, int]]] = None,
        artist_ids: Optional[List[Union[str, int]]] = None,
        playlist_ids: Optional[List[Tuple[Union[str, int], Union[str, int]]]] = None,
        wave_seeds: Optional[List[List[str]]] = None,
        **kwargs: Any,
    ) -> Optional[MusicHistoryItems]:
        """Получение элементов истории прослушивания по списку идентификаторов.

        Args:
            track_ids (:obj:`list` из :obj:`tuple`, optional): Список пар (track_id, album_id).
            album_ids (:obj:`list` из :obj:`str` | :obj:`int`, optional): Список идентификаторов альбомов.
            artist_ids (:obj:`list` из :obj:`str` | :obj:`int`, optional): Список идентификаторов исполнителей.
            playlist_ids (:obj:`list` из :obj:`tuple`, optional): Список пар (uid, kind).
            wave_seeds (:obj:`list` из :obj:`list`, optional): Список массивов семян волны
                (например, ``[['user:onyourwave']]``).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.MusicHistoryItems` | :obj:`None`: Результат запроса
                элементов истории или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/music-history/items'

        items = _build_history_items(track_ids, album_ids, artist_ids, playlist_ids, wave_seeds)

        result = await self._request.post(url, json={'items': items}, **kwargs)

        return MusicHistoryItems.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`music_history`
    musicHistory = music_history
    #: Псевдоним для :attr:`music_history_items`
    musicHistoryItems = music_history_items
