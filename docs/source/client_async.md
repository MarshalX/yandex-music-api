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

<!-- generated-methods -->

## Методы

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Аккаунт
      :link: yandex_music._client_async.account
      :link-type: doc

      ``account_experiments``, ``account_experiments_details``, ``account_settings``, ``account_settings_set``, ``account_status``, ``consume_promo_code``, ``init``, ``permission_alerts``, ``settings``

   .. grid-item-card:: Альбомы
      :link: yandex_music._client_async.albums
      :link-type: doc

      ``albums_similar_entities``, ``albums_trailer``, ``albums_with_tracks``

   .. grid-item-card:: Артисты
      :link: yandex_music._client_async.artists
      :link-type: doc

      ``artists_about``, ``artists_also_albums``, ``artists_brief_info``, ``artists_clips``, ``artists_direct_albums``, ``artists_discography_albums``, ``artists_donation``, ``artists_info``, ``artists_links``, ``artists_safe_direct_albums``, ``artists_similar``, ``artists_skeleton``, ``artists_track_ids``, ``artists_tracks``, ``artists_trailer``

   .. grid-item-card:: Пакетные запросы
      :link: yandex_music._client_async.batch
      :link-type: doc

      ``albums``, ``artists``, ``playlists_list``, ``tracks``

   .. grid-item-card:: Видеоклипы
      :link: yandex_music._client_async.clips
      :link-type: doc

      ``clips``, ``clips_will_like``

   .. grid-item-card:: Концерты
      :link: yandex_music._client_async.concerts
      :link-type: doc

      ``artists_concerts``, ``concert_info``, ``concert_skeleton``, ``concerts_feed``, ``concerts_locations``, ``concerts_tab_config``

   .. grid-item-card:: Авторы контента
      :link: yandex_music._client_async.credits
      :link-type: doc

      ``clips_credits``, ``tracks_credits``

   .. grid-item-card:: Дисклеймеры
      :link: yandex_music._client_async.disclaimers
      :link-type: doc

      ``albums_disclaimer``, ``artists_disclaimer``, ``clips_disclaimer``, ``tracks_disclaimer``

   .. grid-item-card:: Лейблы
      :link: yandex_music._client_async.labels
      :link-type: doc

      ``label``, ``label_albums``, ``label_artists``

   .. grid-item-card:: Лендинг и фид
      :link: yandex_music._client_async.landing
      :link-type: doc

      ``chart``, ``feed``, ``feed_wizard_is_passed``, ``genres``, ``landing``, ``new_playlists``, ``new_releases``, ``podcasts``, ``tags``

   .. grid-item-card:: Лайки и дизлайки
      :link: yandex_music._client_async.likes
      :link-type: doc

      ``users_dislikes_artists``, ``users_dislikes_artists_add``, ``users_dislikes_artists_remove``, ``users_dislikes_tracks``, ``users_dislikes_tracks_add``, ``users_dislikes_tracks_remove``, ``users_likes_albums``, ``users_likes_albums_add``, ``users_likes_albums_remove``, ``users_likes_artists``, ``users_likes_artists_add``, ``users_likes_artists_remove``, ``users_likes_clips``, ``users_likes_clips_add``, ``users_likes_clips_remove``, ``users_likes_playlists``, ``users_likes_playlists_add``, ``users_likes_playlists_remove``, ``users_likes_tracks``, ``users_likes_tracks_add``, ``users_likes_tracks_remove``

   .. grid-item-card:: Метатеги
      :link: yandex_music._client_async.metatags
      :link-type: doc

      ``metatag``, ``metatag_albums``, ``metatag_artists``, ``metatag_playlists``, ``metatags``

   .. grid-item-card:: История прослушивания
      :link: yandex_music._client_async.music_history
      :link-type: doc

      ``music_history``, ``music_history_items``

   .. grid-item-card:: Закреплённые
      :link: yandex_music._client_async.pins
      :link-type: doc

      ``pin_album``, ``pin_artist``, ``pin_playlist``, ``pin_wave``, ``pins``, ``unpin_album``, ``unpin_artist``, ``unpin_playlist``, ``unpin_wave``

   .. grid-item-card:: Плейлисты
      :link: yandex_music._client_async.playlists
      :link-type: doc

      ``playlist``, ``playlist_similar_entities``, ``playlists``, ``playlists_collective_join``, ``playlists_personal``, ``users_playlists``, ``users_playlists_change``, ``users_playlists_create``, ``users_playlists_delete``, ``users_playlists_delete_track``, ``users_playlists_description``, ``users_playlists_insert_track``, ``users_playlists_kinds``, ``users_playlists_list``, ``users_playlists_name``, ``users_playlists_recommendations``, ``users_playlists_trailer``, ``users_playlists_visibility``, ``users_settings``

   .. grid-item-card:: Предсохранения
      :link: yandex_music._client_async.presaves
      :link-type: doc

      ``users_presaves``, ``users_presaves_add``, ``users_presaves_remove``

   .. grid-item-card:: Очередь
      :link: yandex_music._client_async.queue
      :link-type: doc

      ``queue``, ``queue_create``, ``queue_update_position``, ``queues_list``

   .. grid-item-card:: Радио
      :link: yandex_music._client_async.radio
      :link-type: doc

      ``rotor_account_status``, ``rotor_station_feedback``, ``rotor_station_feedback_radio_started``, ``rotor_station_feedback_skip``, ``rotor_station_feedback_track_finished``, ``rotor_station_feedback_track_started``, ``rotor_station_info``, ``rotor_station_settings2``, ``rotor_station_tracks``, ``rotor_stations_dashboard``, ``rotor_stations_list``

   .. grid-item-card:: Поиск
      :link: yandex_music._client_async.search
      :link-type: doc

      ``search``, ``search_suggest``

   .. grid-item-card:: Треки
      :link: yandex_music._client_async.tracks
      :link-type: doc

      ``after_track``, ``play_audio``, ``track_supplement``, ``tracks_download_info``, ``tracks_full_info``, ``tracks_lyrics``, ``tracks_similar``, ``tracks_trailer``

```

```{eval-rst}
.. toctree::
   :hidden:
   :maxdepth: 1

   yandex_music._client_async.account
   yandex_music._client_async.albums
   yandex_music._client_async.artists
   yandex_music._client_async.batch
   yandex_music._client_async.clips
   yandex_music._client_async.concerts
   yandex_music._client_async.credits
   yandex_music._client_async.disclaimers
   yandex_music._client_async.labels
   yandex_music._client_async.landing
   yandex_music._client_async.likes
   yandex_music._client_async.metatags
   yandex_music._client_async.music_history
   yandex_music._client_async.pins
   yandex_music._client_async.playlists
   yandex_music._client_async.presaves
   yandex_music._client_async.queue
   yandex_music._client_async.radio
   yandex_music._client_async.search
   yandex_music._client_async.tracks
```
