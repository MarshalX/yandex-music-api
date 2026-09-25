# 🎮 Удалённый пульт Ynison

Интерактивный пример: выводит текущее состояние плеера (в том числе текущий трек) и позволяет управлять активным устройством (пауза/продолжить, переключение треков, громкость) через модуль {mod}`yandex_music.ynison`.

:::{warning}
Поддержка Ynison находится в **beta-стадии** и может работать нестабильно. Публичное API `yandex_music.ynison` не стабильно: до выхода из беты возможны обратно несовместимые изменения без соблюдения semver. Подробнее — на странице [📡 Ynison](ynison.md).
:::

Установка:
``` bash
pip install -U --pre 'yandex-music[ynison]'
```

```{literalinclude} ../../examples/ynison_remote.py
:language: python
:caption: examples/ynison_remote.py
```
