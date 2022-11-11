# Асинхронный клиент

Приступив к работе первым делом необходимо создать экземпляр клиента.

Инициализация асинхронного клиента:

``` python
from yandex_music import ClientAsync

client = ClientAsync()
await client.init()

# или

client = await Client().init()
```

После успешного создания клиента вы вольны в выборе необходимого метода из API. Все они доступны у объекта класса `ClientAsync` и описаны ниже. Используйте навигацию из меню справа для быстрого доступа.

**Особенности использования асинхронного клиента**

При работе с асинхронной версией библиотеке стоит всегда помнить
следующие особенности:
- Клиент следует импортировать с названием `ClientAsync`, а не просто `Client`.
- При использовании методов-сокращений нужно выбирать метод с суффиксом `_async`.

Пояснение ко второму пункту:

``` python
from yandex_music import ClientAsync

client = await ClientAsync('token').init()
liked_short_track = (await client.users_likes_tracks())[0]

# правильно
full_track = await liked_short_track.fetch_track_async()
await full_track.download_async()

# НЕПРАВИЛЬНО
full_track = await liked_short_track.fetch_track()
await full_track.download()
```

```{eval-rst}
.. include:: yandex_music.client_async.rst
```
