from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, CoverDerivedColors, JSONType


@model
class GenerativeStreamData(YandexMusicModel):
    """Класс, представляющий оформление генеративной станции.

    Attributes:
        title (:obj:`str`, optional): Название станции.
        subtitle (:obj:`str`, optional): Подзаголовок станции.
        background_color (:obj:`str`, optional): Цвет фона в HEX.
        derived_colors (:obj:`yandex_music.CoverDerivedColors`, optional): Производные цвета.
        image_url (:obj:`str`, optional): Ссылка на изображение.
        video_cover_uri (:obj:`str`, optional): Ссылка на видеообложку.
        explanations (:obj:`str`, optional): Описание станции.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    subtitle: Optional[str] = None
    background_color: Optional[str] = None
    derived_colors: Optional['CoverDerivedColors'] = None
    image_url: Optional[str] = None
    video_cover_uri: Optional[str] = None
    explanations: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.image_url)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['GenerativeStreamData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.GenerativeStreamData`: Оформление генеративной станции.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import CoverDerivedColors

        cls_data['derived_colors'] = CoverDerivedColors.de_json(cls_data.get('derived_colors'), client)

        return cls(client=client, **cls_data)
