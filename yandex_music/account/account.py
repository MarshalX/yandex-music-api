from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, PassportPhone


@model
class Account(YandexMusicModel):
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
        child (:obj:`bool`): Дочерний / детский аккаунт (скорее детский, позволяет ограничить
            доступный контент ребенку на Кинопоиске).
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
    passport_phones: List['PassportPhone'] = field(default_factory=list)
    registered_at: Optional[str] = None
    has_info_for_app_metrica: Optional[bool] = None
    child: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        if self.uid:
            self._id_attrs = (self.uid,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Account']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Account`: Основная информация об аккаунте пользователя.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import PassportPhone

        cls_data['passport_phones'] = PassportPhone.de_list(data.get('passport_phones'), client)

        return cls(client=client, **cls_data)  # type: ignore
