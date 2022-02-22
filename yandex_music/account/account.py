from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, PassportPhone


@model
class Account(YandexMusicObject):
    """Класс, представляющий основную информацию об аккаунте пользователя.

    Attributes:
        now (:obj:`str`): Текущая дата и время.
        uid (:obj:`int`, optional): Уникальный идентификатор.
        login (:obj:`str`, optional): Виртуальное имя (обычно e-mail).
        full_name (:obj:`str`, optional): Полное имя (имя и фамилия).
        second_name (:obj:`str`, optional): Фамилия.
        first_name (:obj:`str`, optional): Имя.
        display_name (:obj:`str`, optional): Отображаемое имя.
        service_available (:obj:`bool`): Доступен ли сервис.
        hosted_user (:obj:`bool`, optional): Является ли пользователем чьим-то другим.
        birthday (:obj:`str`, optional): Дата рождения.
        region (:obj:`int`, optional): Регион.
        passport_phones (:obj:`list` из :obj:`yandex_music.PassportPhone`): Мобильные номера.
        registered_at (:obj:`str`, optional): Дата создания учётной записи.
        has_info_for_app_metrica (:obj:`bool`, optional): Наличие информации для App Metrica.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    now: str
    service_available: bool
    region: Optional[int] = None
    uid: Optional[int] = None
    login: Optional[str] = None
    full_name: Optional[str] = None
    second_name: Optional[str] = None
    first_name: Optional[str] = None
    display_name: Optional[str] = None
    hosted_user: Optional[bool] = None
    birthday: Optional[str] = None
    passport_phones: List['PassportPhone'] = None
    registered_at: Optional[str] = None
    has_info_for_app_metrica: bool = False
    client: Optional['Client'] = None

    def __post_init__(self):
        if self.uid:
            self._id_attrs = (self.uid,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Account']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Account`: Основная информация об аккаунте пользователя.
        """
        if not data:
            return None

        data = super(Account, cls).de_json(data, client)
        from yandex_music import PassportPhone

        data['passport_phones'] = PassportPhone.de_list(data.get('passport_phones'), client)

        return cls(client=client, **data)
