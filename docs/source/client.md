# Клиент

Приступив к работе первым делом необходимо создать экземпляр клиента.

Инициализация синхронного клиента:

``` python
from yandex_music import Client

client = Client()
client.init()

# или

client = Client().init()
```

После успешного создания клиента вы вольны в выборе необходимого метода из API. Все они доступны у объекта класса `Client` и описаны ниже. Используйте навигацию из меню справа для быстрого доступа.

```{eval-rst}
.. autoclass:: yandex_music.Client
   :members: __init__, init
   :undoc-members:
   :show-inheritance:
```

<!-- generated-mixins -->

## Миксины

```{eval-rst}
.. toctree::
   :maxdepth: 1

   yandex_music._client.account
   yandex_music._client.albums
   yandex_music._client.artists
   yandex_music._client.batch
   yandex_music._client.clips
   yandex_music._client.concerts
   yandex_music._client.credits
   yandex_music._client.disclaimers
   yandex_music._client.labels
   yandex_music._client.landing
   yandex_music._client.likes
   yandex_music._client.music_history
   yandex_music._client.pins
   yandex_music._client.playlists
   yandex_music._client.presaves
   yandex_music._client.queue
   yandex_music._client.radio
   yandex_music._client.search
   yandex_music._client.tracks
```
