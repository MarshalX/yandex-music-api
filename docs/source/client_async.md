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
.. autoclass:: yandex_music.ClientAsync
   :members: __init__, init
   :undoc-members:
   :show-inheritance:
```

<!-- generated-mixins -->

## Миксины

```{eval-rst}
.. toctree::
   :maxdepth: 1

   yandex_music._client_async.account
   yandex_music._client_async.albums
   yandex_music._client_async.artists
   yandex_music._client_async.batch
   yandex_music._client_async.clips
   yandex_music._client_async.credits
   yandex_music._client_async.disclaimers
   yandex_music._client_async.landing
   yandex_music._client_async.likes
   yandex_music._client_async.music_history
   yandex_music._client_async.pins
   yandex_music._client_async.playlists
   yandex_music._client_async.presaves
   yandex_music._client_async.queue
   yandex_music._client_async.radio
   yandex_music._client_async.search
   yandex_music._client_async.tracks
```
