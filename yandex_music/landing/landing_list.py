from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class LandingList(YandexMusicObject):
    """Класс, представляющий список объектов лендинга.

    Note:
        Известные значения поля `type`: `new-playlists`, `new-releases`, `podcasts`.

        В зависимости от типа будет заполнено то, или иное поле.

    Attributes:
        type (:obj:`str`): Тип результата.
        type_for_from (:obj:`str`): Откуда пришло событие.
        title (:obj:`str`): Заголовок страницы.
        id (:obj:`str`): Уникальный идентификатор списка.
        new_releases (:obj:`list` из :obj:`int`): Новые альбомы.
        new_playlists (:obj:`list` из :obj:`int`): Новые плейлисты.
        podcasts (:obj:`list` из :obj:`int`): Подкасты.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type (:obj:`str`): Тип результата.
        type_for_from (:obj:`str`): Откуда пришло событие.
        title (:obj:`str`): Заголовок страницы.
        id (:obj:`str`, optional): Уникальный идентификатор списка.
        new_releases (:obj:`list` из :obj:`int`, optional): Новые альбомы.
        new_playlists (:obj:`list` из :obj:`int`, optional): Новые плейлисты.
        podcasts (:obj:`list` из :obj:`int`, optional): Подкасты.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self,
        type_: str,
        type_for_from: str,
        title: str,
        id_: Optional[str] = None,
        new_releases: List[int] = None,
        new_playlists: List[int] = None,
        podcasts: List[int] = None,
        client: Optional['Client'] = None,
        **kwargs,
    ) -> None:
        self.type = type_
        self.type_for_from = type_for_from
        self.title = title

        self.id = id_
        self.new_releases = new_releases
        self.new_playlists = new_playlists
        self.podcasts = podcasts

        self.client = client
        self._id_attrs = (self.id, self.new_releases, self.new_playlists, self.podcasts)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Chart']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LandingList`: Список объектов лендинга.
        """
        if not data:
            return None

        data = super(LandingList, cls).de_json(data, client)
        from yandex_music import PlaylistId

        data['new_playlists'] = PlaylistId.de_list(data.get('new_playlists'), client)

        return cls(client=client, **data)
