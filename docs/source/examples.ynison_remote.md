# 🎮 Удалённый пульт Ynison

Интерактивный пример: выводит текущее состояние плеера (в том числе текущий трек) и позволяет управлять активным устройством (пауза/продолжить, переключение треков, громкость) через модуль {mod}`yandex_music.ynison`.

Пример держит одно постоянное соединение через {class}`YnisonClient <yandex_music.ynison.client.YnisonClient>`: состояние обновляется в фоне, а команды отправляются без переподключения. Если на аккаунте ничего не играет или очередь закончилась, пример сообщит об этом и продолжит работу. Подробнее на странице [📡 Ynison](ynison.md).

Установка:
``` bash
pip install -U 'yandex-music[ynison]'
```

Запуск:
``` bash
TOKEN=<ваш токен> python ynison_remote.py
```

```{literalinclude} ../../examples/ynison_remote.py
:language: python
:caption: examples/ynison_remote.py
```
