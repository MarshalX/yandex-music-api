from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.skeleton.skeleton_source import SkeletonSource
    from yandex_music.skeleton.skeleton_tab import SkeletonTab
    from yandex_music.skeleton.skeleton_view_all_action import SkeletonViewAllAction


@model
class SkeletonBlockData(YandexMusicModel):
    """Класс, представляющий данные блока скелетона.

    Note:
        Для блока типа ``TABS`` заполняются поля ``tabs`` и ``selected_tab_index``.
        Для остальных блоков заполняются ``source``, ``title``, ``show_policy``, ``view_all_action``.

    Attributes:
        tabs (:obj:`list` из :obj:`yandex_music.SkeletonTab`, optional): Список вкладок.
        selected_tab_index (:obj:`int`, optional): Индекс выбранной вкладки.
        source (:obj:`yandex_music.SkeletonSource`, optional): Источник данных.
        title (:obj:`str`, optional): Заголовок блока.
        show_policy (:obj:`str`, optional): Политика отображения.
        view_all_action (:obj:`yandex_music.SkeletonViewAllAction`, optional): Действие «Показать все».
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tabs: Optional[List['SkeletonTab']] = None
    selected_tab_index: Optional[int] = None
    source: Optional['SkeletonSource'] = None
    title: Optional[str] = None
    show_policy: Optional[str] = None
    view_all_action: Optional['SkeletonViewAllAction'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.tabs, self.source, self.title)
