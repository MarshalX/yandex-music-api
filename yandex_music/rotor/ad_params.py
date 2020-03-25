from typing import TYPE_CHECKING, Optional, Union

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class AdParams(YandexMusicObject):
    """Класс, представляющий параметры рекламного объявления.

    Note:
        Известные дополнительные параметры(`other_params`): `user:{ID}`.

    Attributes:
        partner_id (:obj:`str` | :obj:`int`): Уникальный идентификатор заказчика рекламы.
        category_id (:obj:`str` | :obj:`int`): Уникальный идентификатор категории рекламы.
        page_ref (:obj:`str`): Ссылка на ссылающуюся страницу.
        target_ref (:obj:`str`): Ссылка на целевую страницу.
        other_params (:obj:`str`): Другие параметры.
        ad_volume (:obj:`int`): Громкость воспроизводимой рекламы.
        genre_id (:obj:`str`): Уникальный идентификатор жанра.
        genre_name (:obj:`str`): Название жанра.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        partner_id (:obj:`str` | :obj:`int`): Уникальный идентификатор заказчика рекламы.
        category_id (:obj:`str` | :obj:`int`): Уникальный идентификатор категории рекламы.
        page_ref (:obj:`str`): Ссылка на ссылающуюся страницу.
        target_ref (:obj:`str`): Ссылка на целевую страницу.
        other_params (:obj:`str`): Другие параметры.
        ad_volume (:obj:`int`): Громкость воспроизводимой рекламы.
        genre_id (:obj:`str`, optional): Уникальный идентификатор жанра.
        genre_name (:obj:`str`, optional): Название жанра.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 partner_id: Union[str, int],
                 category_id: Union[str, int],
                 page_ref: str,
                 target_ref: str,
                 other_params: str,
                 ad_volume: int,
                 genre_id: Optional[str] = None,
                 genre_name: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.partner_id = partner_id
        self.category_id = category_id
        self.page_ref = page_ref
        self.target_ref = target_ref
        self.other_params = other_params
        self.ad_volume = ad_volume

        self.genre_id = genre_id
        self.genre_name = genre_name

        self.client = client
        self._id_attrs = (self.partner_id, self.category_id, self.page_ref,
                          self.target_ref, self.other_params, self.ad_volume)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['AdParams']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.AdParams`: Параметры рекламного объявления.
        """
        if not data:
            return None

        data = super(AdParams, cls).de_json(data, client)

        return cls(client=client, **data)
