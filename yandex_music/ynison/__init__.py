"""Ynison — протокол реального состояния плеера Яндекс Музыки.

Подпакет требует дополнительных зависимостей `[ynison]` (betterproto, websockets)
и не импортируется основным пакетом :mod:`yandex_music`. Пользователи, которым
Ynison не нужен, могут не устанавливать эти зависимости.
"""

_missing_ynison_deps = []
try:
    import betterproto  # noqa: F401
except ImportError:
    _missing_ynison_deps.append('betterproto')
try:
    import websockets  # noqa: F401
except ImportError:
    _missing_ynison_deps.append('websockets')

if _missing_ynison_deps:
    raise ImportError(
        'Для работы Ynison нужны дополнительные зависимости: '
        f'{", ".join(_missing_ynison_deps)}. '
        "Установите их командой: pip install 'yandex-music[ynison]'"
    )

del _missing_ynison_deps

from yandex_music.ynison import messages, models, simple, simple_async  # noqa: E402
from yandex_music.ynison._client import YnisonClient, YnisonClientAsync  # noqa: E402

__all__ = [
    'YnisonClient',
    'YnisonClientAsync',
    'messages',
    'models',
    'simple',
    'simple_async',
]
