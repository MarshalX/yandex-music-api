from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Id, Icon, Restrictions


class Station(YandexMusicObject):
    """Класс, представляющий станцию.

    Note:
        `id_for_from` обозначает предка станции, например, жанр, настроение или занятие.
        Неизвестно когда используется `id_for_from`, а когда `parent_id`.

    Attributes:
        id (:obj:`yandex_music.Id`): Уникальный идентификатор станции.
        name (:obj:`str`): Название станции.
        icon (:obj:`yandex_music.Icon`): Иконка станции.
        mts_icon (:obj:`yandex_music.Icon`): Иконка TODO.
        geocell_icon (:obj:`yandex_music.Icon`): Иконка TODO.
        id_for_from (:obj:`str`): Категория (тип) станции.
        restrictions (:obj:`yandex_music.Restrictions`): Ограничения для настроек станции старого формата.
        restrictions2 (:obj:`yandex_music.Restrictions`): Ограничения для настроек станции.
        parent_id (:obj:`yandex_music.Id`): Уникальный идентификатор станции, являющейся предком текущей.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

    Args:
        id_ (:obj:`yandex_music.Id`): Уникальный идентификатор станции.
        name (:obj:`str`): Название станции.
        icon (:obj:`yandex_music.Icon`): Иконка станции.
        mts_icon (:obj:`yandex_music.Icon`): Иконка TODO.
        geocell_icon (:obj:`yandex_music.Icon`): Иконка TODO.
        id_for_from (:obj:`str`): Категория (тип) станции.
        restrictions (:obj:`yandex_music.Restrictions`): Ограничения для настроек станции старого формата.
        restrictions2 (:obj:`yandex_music.Restrictions`): Ограничения для настроек станции.
        parent_id (:obj:`yandex_music.Id`, optional): Уникальный идентификатор станции, являющейся предком текущей.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: Optional['Id'],
                 name: str,
                 icon: Optional['Icon'],
                 mts_icon: Optional['Icon'],
                 geocell_icon: Optional['Icon'],
                 id_for_from: str,
                 restrictions: Optional['Restrictions'],
                 restrictions2: Optional['Restrictions'],
                 parent_id: Optional['Id'] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.name = name
        self.icon = icon
        self.mts_icon = mts_icon
        self.geocell_icon = geocell_icon
        self.id_for_from = id_for_from
        self.restrictions = restrictions
        self.restrictions2 = restrictions2

        self.parent_id = parent_id

        self.client = client
        self._id_attrs = (self.id, self.name, self.icon, self.mts_icon, self.geocell_icon,
                          self.id_for_from, self.restrictions, self.restrictions2)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Station']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Station`: Станция.
        """
        if not data:
            return None

        data = super(Station, cls).de_json(data, client)
        from yandex_music import Id, Icon, Restrictions
        data['id_'] = Id.de_json(data.get('id_'), client)
        data['parent_id'] = Id.de_json(data.get('parent_id'), client)
        data['icon'] = Icon.de_json(data.get('icon'), client)
        data['mts_icon'] = Icon.de_json(data.get('mts_icon'), client)
        data['geocell_icon'] = Icon.de_json(data.get('geocell_icon'), client)
        data['restrictions'] = Restrictions.de_json(data.get('restrictions'), client)
        data['restrictions2'] = Restrictions.de_json(data.get('restrictions2'), client)

        return cls(client=client, **data)
