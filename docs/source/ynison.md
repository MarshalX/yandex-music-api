# 📡 Ynison

Ynison это внутренний элемент Яндекс Музыки, по которому приложения синхронизируют состояние плеера между устройствами и управляют воспроизведением удалённо (пауза/продолжить, переключение трека, громкость, список подключённых устройств).

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

Каждый вызов открывает новое соединение, поэтому для серии команд или подписки на изменения удобнее [постоянное соединение](#постоянное-соединение).

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

{class}`YnisonClient <yandex_music.ynison.client.YnisonClient>` (блокирующий) и {class}`YnisonClientAsync <yandex_music.ynison.client_async.YnisonClientAsync>` (корутины) держат одно соединение и предоставляют одинаковый интерфейс. Проще всего работать через контекстный менеджер `session()`: он подключается, дожидается первого состояния от сервера и отключается при выходе из блока.

``` python
from yandex_music.ynison import YnisonClient

with YnisonClient(token).session() as client:
    print(client.current_playable.title)
    print(client.active_device.info.title)

    client.pause()
    client.next_track()
    client.set_volume(0.5)
```

``` python
import asyncio
from yandex_music.ynison import YnisonClientAsync

async def main():
    async with YnisonClientAsync(token).session() as client:
        print(client.current_playable.title)
        await client.resume()

asyncio.run(main())
```

Команды управления:

- `pause()`, `resume()`: пауза и продолжение на активном устройстве. Текущая позиция трека сохраняется.
- `next_track()`, `previous_track()`: переключение трека с учётом перемешивания.
- `set_volume(volume, target_device_id=None)`: громкость от `0.0` до `1.0` на активном или указанном устройстве.
- `send(request)`: отправка произвольного `PutYnisonStateRequest`, собранного билдерами из {mod}`yandex_music.ynison.messages`.

Свойства:

- `state`: последнее состояние; если оно ещё не получено, выбрасывает исключение.
- `latest_state`: последнее состояние или `None`.
- `current_playable`, `active_device`: текущий трек и активное устройство или `None`.
- `device_id`: идентификатор этого клиента в Ynison-сессии.
- `is_running`: запущен ли цикл подключения.

Конструктор принимает `token`, `device_id=None`, `device_title='Python SDK'` (название, которое увидят другие устройства) и `max_reconnect_attempts=None`.

### Подписка на изменения

`on_state(listener)` вызывает listener на каждое новое состояние, `on_error(listener)` вызывает его на нетерминальные ошибки: отклонённый сервером запрос и потерю соединения перед переподключением. Оба метода можно использовать как декораторы, `remove_listener(listener)` снимает подписку. Исключения в listener'ах пишутся в логгер `yandex_music.ynison` и не прерывают приём состояний.

Для длительной работы вызовите `connect()`: он блокирует поток (или ожидает, в асинхронном клиенте) до вызова `disconnect()`. После отключения клиента можно подключить снова.

``` python
import threading
from yandex_music.ynison import YnisonClient

client = YnisonClient(token)

@client.on_state
def log(state):
    track = client.current_playable
    print('сейчас играет:', track.title if track else '-')

@client.on_error
def log_error(error):
    print('ошибка Ynison:', error)

threading.Thread(target=client.connect, daemon=True).start()
# ... client.pause(), client.next_track() и т.д. ...
client.disconnect()
```

В асинхронном клиенте listener'ы могут быть корутинами. Они вызываются по очереди внутри цикла приёма, поэтому долгие операции лучше выносить в отдельные задачи. Асинхронного клиента можно создать вне запущенного event loop.

### Переподключение

При обрыве соединения клиент переподключается сам, каждый раз заново получая адрес сервера. Паузы между попытками берутся из рекомендаций сервера, а keepalive-пинги настраиваются по параметрам, которые присылает сервер. `max_reconnect_attempts` ограничивает число неудачных попыток подряд; после превышения `connect()` выбрасывает последнюю ошибку.

Не переподключаются после неверного или истёкшего токена ({class}`~yandex_music.exceptions.YnisonUnauthorizedError`), вытеснения другим клиентом ({class}`~yandex_music.exceptions.YnisonDeviceDisplacedError`) и ошибок, после которых сервер просит не возвращаться какое-то время. Такие ошибки выбрасываются из `connect()` и `session()`.

## Идентификатор устройства

Каждый клиент подключается к Ynison как отдельное устройство со своим `device_id`. **Один `device_id` может использоваться только одним живым подключением**: если подключиться второй раз с тем же идентификатором, сервер закроет первое соединение, и оно завершится с {class}`~yandex_music.exceptions.YnisonDeviceDisplacedError`.

По умолчанию `device_id` не случайный, а вычисляется из токена. Поэтому повторные запуски скрипта не плодят новые устройства в сессии. Функции `simple` и `simple_async` используют свой отдельный идентификатор по умолчанию и не вытесняют долгоживущий `YnisonClient`. Чтобы держать несколько подключений одновременно, передайте каждому свой `device_id`, например {func}`messages.generate_device_id() <yandex_music.ynison.messages.generate_device_id>`.

## Ошибки

Все исключения модуля наследуются от {class}`~yandex_music.exceptions.YnisonError`:

| Исключение | Когда выбрасывается |
|------------|---------------------|
| {class}`~yandex_music.exceptions.YnisonTimeoutError` | Сервер не прислал начальное состояние за `timeout` секунд. |
| {class}`~yandex_music.exceptions.YnisonConnectionClosedError` | Отправка команды без активного соединения или в закрытое соединение. |
| {class}`~yandex_music.exceptions.YnisonNoActiveDeviceError` | `pause`, `resume` или `set_volume` без активного (играющего) устройства. |
| {class}`~yandex_music.exceptions.YnisonQueueBoundaryError` | `next_track` на последнем треке очереди или `previous_track` на первом. |
| {class}`~yandex_music.exceptions.YnisonServerError` | Ошибка, присланная сервером. Атрибуты: `message`, `grpc_code`, `http_code`, `error_code`, `backoff_ms`, `go_away_seconds`. |
| {class}`~yandex_music.exceptions.YnisonUnauthorizedError` | Неверный или истёкший токен (наследник `YnisonServerError`). |
| {class}`~yandex_music.exceptions.YnisonDeviceDisplacedError` | Подключился другой клиент с тем же `device_id` (наследник `YnisonServerError`). |

``` python
from yandex_music.exceptions import YnisonNoActiveDeviceError, YnisonQueueBoundaryError

try:
    client.next_track()
except YnisonQueueBoundaryError:
    print('это последний трек')
except YnisonNoActiveDeviceError:
    print('сейчас ничего не играет')
```

## Состояние и хелперы

Состояние от сервера представлено моделью {class}`~yandex_music.ynison.models.ynison_state.PutYnisonStateResponse`, доступная также под коротким именем `YnisonState` (`from yandex_music.ynison import YnisonState`). Основные модели (`Playable`, `Device`, `PlayerQueue`, `PlayingStatus` и другие) можно импортировать прямо из `yandex_music.ynison.models`.

Модуль {mod}`yandex_music.ynison.utils` содержит хелперы для типовых вычислений над состоянием:

- `get_current_playable(state)`: текущий трек очереди.
- `get_active_device(state)`: активное устройство.
- `get_playback_order(queue)`: порядок воспроизведения с учётом перемешивания.
- `get_neighbour_index(queue, delta)`: индекс следующего или предыдущего трека.
- `get_current_progress_ms(status)`: актуальная позиция трека. Сервер присылает позицию на момент последнего изменения, хелпер досчитывает прошедшее с тех пор время.

``` python
from yandex_music.ynison import utils

with YnisonClient(token).session() as client:
    status = client.state.player_state.status
    print(f'{utils.get_current_progress_ms(status)} / {status.duration_ms} мс')
```

Полный интерактивный пример: [удалённый пульт Ynison](examples.ynison_remote.md).

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`broadcast;1em;sd-mr-1` Синхронный клиент
      :link: yandex_music.ynison.client
      :link-type: doc

      ``YnisonClient``: ``session``, ``connect``/``disconnect``, ``pause``/``resume``, ``next_track``/``previous_track``, ``set_volume``, ``on_state``/``on_error``.

   .. grid-item-card:: :octicon:`broadcast;1em;sd-mr-1` Асинхронный клиент
      :link: yandex_music.ynison.client_async
      :link-type: doc

      ``YnisonClientAsync``: тот же интерфейс, операции ввода-вывода являются корутинами.

   .. grid-item-card:: :octicon:`tools;1em;sd-mr-1` Хелперы состояния
      :link: yandex_music.ynison.utils
      :link-type: doc

      ``get_current_playable``, ``get_active_device``, ``get_playback_order``, ``get_neighbour_index``, ``get_current_progress_ms``

   .. grid-item-card:: :octicon:`file-code;1em;sd-mr-1` Билдеры сообщений
      :link: yandex_music.ynison.messages
      :link-type: doc

      ``build_full_state_request``, ``build_set_paused_request``, ``build_change_track_request``, ``build_next_track_request``, ``build_previous_track_request``, ``build_set_volume_request``, ``generate_device_id``

   .. grid-item-card:: :octicon:`file-binary;1em;sd-mr-1` Модели
      :link: yandex_music.ynison.models
      :link-type: doc

      Модели: ``YnisonState``, ``Playable``, ``Device``, ``PutYnisonStateRequest``/``Response``, ``PlayingStatus``, ``PlayerQueue`` и т.д.
```

```{eval-rst}
.. toctree::
   :hidden:
   :maxdepth: 1

   yandex_music.ynison.simple
   yandex_music.ynison.simple_async
   yandex_music.ynison.client
   yandex_music.ynison.client_async
   yandex_music.ynison.utils
   yandex_music.ynison.messages
   yandex_music.ynison.models
```
