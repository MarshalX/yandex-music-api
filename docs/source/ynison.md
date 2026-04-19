# 📡 Ynison

Ynison это внутренний элемент Яндекс Музыки, по которому приложения синхронизируют состояние плеера между устройствами и управляют воспроизведением удалённо (пауза/продолжить, переключение трека, громкость, список подключённых устройств).

:::{warning}
Поддержка Ynison находится в **beta-стадии** и может работать нестабильно: возможны разрывы соединений, задержки и граничные случае, которые ещё не отловлены.

Публичное API модуля `yandex_music.ynison` **не стабильно**. Пока статус beta, в нём могут появляться **обратно несовместимые изменения без соблюдения semver**: переименования, изменения сигнатур, реорганизация модулей. Если работаете на конкретной версии библиотеки, то пиньте её в `requirements.txt` и читайте [CHANGES.md](changes.md) перед обновлением.

Сообщайте о проблемах в [трекер проекта](https://github.com/MarshalX/yandex-music-api/issues). Это поможет быстрее довести интерфейс до стабильного состояния.
:::

## Установка

Модуль требует дополнительных зависимостей и по умолчанию не устанавливается:

``` bash
pip install 'yandex-music[ynison]'
```

Без этих зависимостей основная библиотека продолжит работать, только попытка импортировать `yandex_music.ynison` приведёт к явному `ImportError` с инструкцией по установке.

## Простые интерфейсы

Разовые функции для типичных сценариев «открыть соединение, выполнить одно действие, закрыть». Блокирующие в `simple` и корутины в `simple_async`.

``` python
from yandex_music.ynison import simple

track = simple.get_current_track(token)
simple.pause(token)
simple.next_track(token)
```

``` python
import asyncio
from yandex_music.ynison import simple_async

async def main():
    track = await simple_async.get_current_track(token)
    await simple_async.pause(token)

asyncio.run(main())
```

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`sync;1em;sd-mr-1` Синхронный интерфейс
      :link: yandex_music.ynison.simple
      :link-type: doc

      ``get_state``, ``get_current_track``, ``get_devices``, ``get_active_device``, ``pause``, ``resume``, ``next_track``, ``previous_track``, ``set_volume``

   .. grid-item-card:: :octicon:`zap;1em;sd-mr-1` Асинхронный интерфейс
      :link: yandex_music.ynison.simple_async
      :link-type: doc

      ``get_state``, ``get_current_track``, ``get_devices``, ``get_active_device``, ``pause``, ``resume``, ``next_track``, ``previous_track``, ``set_volume``
```

## Постоянное соединение

Для подписки на поток состояния и отправки произвольных `PutYnisonStateRequest` используйте {class}`yandex_music.ynison.YnisonClient` (блокирующий) или {class}`yandex_music.ynison.YnisonClientAsync` (корутины). Оба класса предоставляют одинаковые интерфейсы:

- `on_state(listener)` — подписка на фреймы состояния.
- `send(request)` — отправка произвольного `PutYnisonStateRequest`.
- `latest_state`, `device_id` — свойства для чтения состояния.
- `disconnect()` — остановка подключения.
- `session(timeout)` — контекстный менеджер для разового цикла connect → одно действие → disconnect.

``` python
import threading
from yandex_music.ynison import YnisonClient, messages

client = YnisonClient(token)

@client.on_state
def log(state):
    print('rid:', state.rid)

threading.Thread(target=client.connect, daemon=True).start()
# ... далее самостоятельно строите request через messages.* и вызываете client.send(...)
```

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`broadcast;1em;sd-mr-1` Синхронный клиент
      :link: yandex_music.ynison._client.client
      :link-type: doc

      ``YnisonClient`` — connect/disconnect/send/on_state/session в блокирующем режиме.

   .. grid-item-card:: :octicon:`broadcast;1em;sd-mr-1` Асинхронный клиент
      :link: yandex_music.ynison._client.client_async
      :link-type: doc

      ``YnisonClientAsync`` — connect/disconnect/send/on_state/session корутины.

   .. grid-item-card:: :octicon:`file-code;1em;sd-mr-1` Билдеры сообщений
      :link: yandex_music.ynison.messages
      :link-type: doc

      ``get_update_full_state_request``, ``get_set_paused_request``, ``get_change_track_request``, ``get_next_track_request``, ``get_prev_track_request``, ``get_set_volume_request``

   .. grid-item-card:: :octicon:`file-binary;1em;sd-mr-1` Модели
      :link: yandex_music.ynison.models
      :link-type: doc

      Модели: ``Playable``, ``Device``, ``PutYnisonStateRequest``/``Response``, ``PlayingStatus``, ``PlayerQueue`` и т.д.
```

```{eval-rst}
.. toctree::
   :hidden:
   :maxdepth: 1

   yandex_music.ynison.simple
   yandex_music.ynison.simple_async
   yandex_music.ynison._client.client
   yandex_music.ynison._client.client_async
   yandex_music.ynison.messages
   yandex_music.ynison.models
```
