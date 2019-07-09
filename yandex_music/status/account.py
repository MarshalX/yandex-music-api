from datetime import datetime

from yandex_music import YandexMusicObject


class Account(YandexMusicObject):
    """Класс предоставляющий основную информацию об аккаунте пользователя.

    Attributes:
        now (:obj:`datetime.datetime`): Текущая дата и время.
        uid (:obj:`int`): Уникальный идентификатор.
        login (:obj:`str`): Виртуальное имя (обычно e-mail).
        full_name (:obj:`str`): Полное имя (имя и фамилия).
        second_name (:obj:`str`): Фамилия.
        first_name (:obj:`str`): Имя.
        display_name (:obj:`str`): Отображаемое имя.
        birthday (:obj:`datetime.datetime`): Дата рождения.
        service_available (:obj:`bool`): Доступен ли сервис.
        hosted_user (:obj:`bool`): Является ли пользователем чьим-то другим.
        region (:obj:`int`): Регион.
        passport_phones (:obj:`list` из :obj:`yandex_music.PassportPhone`): Список объектов класса
            :class:`yandex_music.PassportPhone` представляющие мобильные номера.
        registered_at (:obj:`datetime.datetime`): Дата создания аккаунта.
        has_info_for_app_metrica (:obj:`bool`): Наличие информации для App Metrica.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        now (:obj:`str`): Текущая дата и время.
        uid (:obj:`int`): Уникальный идентификатор.
        login (:obj:`str`): Виртуальное имя (обычно e-mail).
        full_name (:obj:`str`): Полное имя (имя и фамилия).
        second_name (:obj:`str`): Фамилия.
        first_name (:obj:`str`): Имя.
        display_name (:obj:`str`): Отображаемое имя.
        service_available (:obj:`bool`): Доступен ли сервис.
        hosted_user (:obj:`bool`): Является ли пользователем чьим-то другим.
        birthday (:obj:`str`, optional): Дата рождения.
        region (:obj:`int`, optional): Регион.
        passport_phones (:obj:`list` из :obj:`yandex_music.PassportPhone`): Список объектов класса
            :class:`yandex_music.PassportPhone` представляющие мобильные номера.
        registered_at (:obj:`str`, optional): Дата создания учётной записи.
        has_info_for_app_metrica (:obj:`bool`, optional): Наличие информации для App Metrica.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 now,
                 uid,
                 login,
                 full_name,
                 second_name,
                 first_name,
                 display_name,
                 service_available,
                 hosted_user,
                 birthday=None,
                 region=None,
                 passport_phones=None,
                 registered_at=None,
                 has_info_for_app_metrica=False,
                 client=None,
                 **kwargs):
        self.now = datetime.fromisoformat(now)
        self.uid = uid
        self.login = login
        self.region = region
        self.full_name = full_name
        self.second_name = second_name
        self.first_name = first_name
        self.display_name = display_name
        self.service_available = service_available
        self.hosted_user = hosted_user
        self.passport_phones = passport_phones

        self.birthday = datetime.fromisoformat(birthday) if birthday else None
        self.registered_at = datetime.fromisoformat(registered_at) if registered_at else registered_at
        self.has_info_for_app_metrica = has_info_for_app_metrica

        self.client = client
        self._id_attrs = (self.uid,)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Account`: Объект класса :class:`yandex_music.Account`.
        """
        if not data:
            return None

        data = super(Account, cls).de_json(data, client)
        from yandex_music import PassportPhone
        data['passport_phones'] = PassportPhone.de_list(data.get('passport_phones'), client)

        return cls(client=client, **data)
