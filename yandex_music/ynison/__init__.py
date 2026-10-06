"""Ynison: протокол реального состояния плеера Яндекс Музыки.

Подпакет требует дополнительных зависимостей `[ynison]` (betterproto, websockets)
и не импортируется основным пакетом :mod:`yandex_music`. Пользователи, которым
Ynison не нужен, могут не устанавливать эти зависимости.
"""

from typing import List

_missing_ynison_deps: List[str] = []
try:
    import betterproto  # noqa: F401
except ImportError:
    _missing_ynison_deps.append('betterproto')
try:
    import websockets.asyncio.client
    import websockets.sync.client  # noqa: F401
except ImportError:
    _missing_ynison_deps.append('websockets>=13')

if len(_missing_ynison_deps) > 0:
    raise ImportError(
        'Для работы Ynison нужны дополнительные зависимости: '
        f'{", ".join(_missing_ynison_deps)}. '
        "Установите их командой: pip install -U 'yandex-music[ynison]'"
    )

del _missing_ynison_deps

from yandex_music.ynison import messages, models, simple, simple_async, utils  # noqa: E402
from yandex_music.ynison.client import YnisonClient  # noqa: E402
from yandex_music.ynison.client_async import YnisonClientAsync  # noqa: E402
from yandex_music.ynison.models import YnisonState  # noqa: E402

__all__ = [
    'YnisonClient',
    'YnisonClientAsync',
    'YnisonState',
    'messages',
    'models',
    'simple',
    'simple_async',
    'utils',
]
