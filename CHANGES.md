# Список изменений

## Версия 2.1.0

**23.04.2023**

**Переломные изменения**

При работе над [#547](https://github.com/MarshalX/yandex-music-api/issues/547) и
[#550](https://github.com/MarshalX/yandex-music-api/issues/550) 
были удалены `*args` параметры, у методов класса `Client`, которые не имели никакого эффекта. 
Передать через позиционные аргументы что-то в конечный запрос не было возможно. 
Удаление данной конструкции **могло** затронуть код в котором ошибочно передавались лишние аргументы.
При корректном использовании библиотеки новая версия полностью совместима со старым кодом.

**Крупные изменения**

- Добавлена поддержка Python 3.11.
- В модели добавлены методы `download_bytes` и `download_bytes_async`, для получения файлов в виде байтов ([#539](https://github.com/MarshalX/yandex-music-api/issues/539)).
- Добавлен новый метод получения текста и синхронного текста треков ([#568](https://github.com/MarshalX/yandex-music-api/pull/568)).
- Добавлена возможность задать `timeout` по умолчанию для `Client` ([#362](https://github.com/MarshalX/yandex-music-api/issues/362)).
- Использование настройки языка клиента во всех методах ([#554](https://github.com/MarshalX/yandex-music-api/issues/554)).
- Добавлено поле `preview_description` классу `GeneratedPlaylist`.
- Добавлены поля `pretrial_active` и `userhash` классу `Status`.
- Добавлено поле `had_any_subscription` классу `Subscription`.
- Добавлено поле `child` классу `Account`.
- Добавлены новые поля `up_title`, `rup_description`, `custom_name` классу `StationResult`.
- Добавлены новые модели: `CustomWave`, `R128`, `LyricsInfo`.
- Классу `Track` добавлены новые поля: `track_source`, `available_for_options`, `r128`, `lyrics_info`, `track_sharing_flag`.
- Классу `TrackShort` добавлены новые поля: `original_index`.
- Классу `Playlist` добавлены новые поля: `custom_wave`, `pager`.
- Классу `Album` добавлены новые поля: `available_for_options`.
- Поле `cover_white` класса `MixLink` теперь опциональное.

**Незначительные изменения и/или исправления**

- Добавлен генератор Camel Case псевдонимов для методов ([#542](https://github.com/MarshalX/yandex-music-api/issues/542)).
- Добавлен Makefile с сокращениями удобными при разработке библиотеки.
- Добавлено отображение модуля при нахождении неизвестного поля.
- Добавлена поддержка MD файлов для документации.
- Добавлена страница в документацию по получению токена.
- Добавлены примеры в документацию.
- Переделана структура и обновлена документации.
- Исправлен запуск генератора async клиента на Windows.
- Исправлен метод `fetch_tracks_async` у класса `Playlist`.
- Исправлены type hints у декоратора `log`.
- Исправлены type hints для `SearchResult` в классе `Search`.
- Исправлено отображение название класса в `report_unknown_fields_callback`.
- Исправлены методы-сокращения `like` и `dislike` класса `Playlist` ([#516](https://github.com/MarshalX/yandex-music-api/pull/516)).

## Версия 2.0.0

**23.02.2022**

**Поддержка asyncio и модели на dataclasses**

**Переломные изменения**

- Убрана поддержка `Python 3.6`.
- Удалено получение авторизационного токена по логину и паролю (метод `from_credentials` класса `Client`).
- Удалена возможность задать свой обработчик на полученные неизвестные поля от API (аргумент `report_new_fields_callback` конструктора класса `Client`.
- Удалён аргумент `fetch_account_status` из конструктора класса `Client`. Теперь необходимо вызывать метод `init` для получения ID аккаунта который будет использоваться в последующих запросах. В противном случае передача `user_id` при вызове многих методов класса `Client` становится обязательной.
- Исключение `BadRequest` переименовано в `BadRequestError`.
- Исключение `Unauthorized` переименовано в `UnauthorizedError`.
- Исключение `InvalidBitrate` переименовано в `InvalidBitrateError`.
- Исключение `TimedOut` переименовано в `TimedOutError`.
- Свойство `result` класса `Response` удалено. Вместо него добавлен метод `get_result`.
- Свойство `error` класса `Response` удалено. Вместо него добавлен метоl `get_error`.
- В JSON представлении моделей к полям, чьё имя совпадает с именем стандартных функций, больше не добавляется нижнее подчеркивание в конец (пример: `id`, а не `id_`; `max`, а не `max_`). Теперь нижнее подчеркивание добавляется только к зарезервированным словам (пример: `from` будет `from_`).

**Крупные изменения**

- Добавлена асинхронная версия клиента и всех методов-сокращений (класс `ClientAsync`).
- Добавлено новое исключение `NotFoundError` (наследник `NetworkError`). Будет сгенерировано при получении статус кода 404.
- Проект больше не использует `pipenv`.
- Зависимости проекта больше не требуют конкретных версий.
- Для генерации исходных файлов `Sphinx` теперь используется `sphinx-apidoc`.

**Незначительные изменения и/или исправления**

- Исправлена обработка серверных ошибок которые вернулись в отличном от JSON формате.
- Исправлена обработка серверных ошибок метода `search` класса `Client`.
- Предупреждения о пришедших неизвестных полях от API отключены по умолчанию.
- Используется английская локализация `Sphinx`.
- Изменена тема документации.

## Версия 1.0.0

**06.02.2021**

**Стабильная версия библиотеки**

**Переломные изменения**

- Поле `error` класса `Artist` теперь называется `reason`.
- Метод `users_playlists` класса `Client` теперь возвращает один объект плейлиста, когда был передан один `kind`. При передаче списка в `kind` вернётся список плейлистов ([#318](https://github.com/MarshalX/yandex-music-api/issues/318)).
- Поле `labels` класса `Album` теперь может содержать список из строк, а не только список объектов класса `Label`.

**Крупные изменения**

- Добавлены примеры в папку `examples`.
- **Добавлена поддержка рекомендаций для плейлистов ([#324](https://github.com/MarshalX/yandex-music-api/issues/324))**:
  - Добавлен класс `PlaylistRecommendations`.
  - Добавлен метод клиента для получения рекомендаций(`users_playlists_recommendations`).
  - Добавлен метод `get_recommendations` классу `Playlist` для
- **Добавлено получение чартов ([#294](https://github.com/MarshalX/yandex-music-api/issues/294))**:
  - Добавлены новые классы: `ChartInfo`, `ChartInfoMenu`,`ChartInfoMenuItem`.
  - Добавлен метод клиента для получения чарта (`chart`).
- **Добавлена поддержка тегов/подборок ([#192](https://github.com/MarshalX/yandex-music-api/issues/192))**:
  - Добавлены новые классы: `TagResult`, `Tag`.
  - Добавлен новый метод клиента для получения тегов (`tags`).
- **Добавлено присоединение к коллективному плейлисту ([#317](https://github.com/MarshalX/yandex-music-api/issues/317))**:
  - Добавлен новый метод клиента для присоединения(`playlists_collective_join`).
- **Добавлена поддержка очередей прослушивания ([#246](https://github.com/MarshalX/yandex-music-api/issues/246))**:
  - Добавлены новые классы: `Context`, `Queue`, `QueueItem`.
  - Добавлены новые методы в `Client`: `queues_list`, `queue`,`queue_update_position`, `queue_create`.
  - Добавлены поля `track_id` и `from_` в класс `TrackId`.
  - Добавлена возможность смены языка у клиента для ответов от API.
  - Добавлена десериализация любого объекта в `JSON` пригодного для отправки в запросе на Яндекс API.
- **Добавлены следующие методы для `Client`**:
  - `new_releases` – получение полного списка всех новых релизов.
  - `new_playlists` – получение полного списка всех новый плейлистов.
  - `podcasts` – получение подкаста с лендинга.
- **Добавлены новые сокращения в модели**:
  - `download_cover_white`, `download_cover_uri` в `MixLink`.
  - `download_image` в `Promotion`.
  - `artists_name` в `Album` и `Track`.
  - `fetch_track`, `track_full_id` в `TrackId`.
  - `fetch_tracks` в `TracksList`.
  - `insert_track`, `delete_tracks`, `delete` в `Playlist`.
  - `playlist_id`, `fetch_playlist` в `PlaylistId`.
  - `get_current_track` в `Queue`.
  - `fetch_queue` в `QueueItem`.
  - `next_page`, `get_page`, `prev_page` в `Search`.
  - и другие...
- Добавлена поддержка новых типов поиска: подкасты, выпуски, пользователи.
- Добавлен callback для обработки новых полей.
- Добавлена информацию по поводу запуска потока по треку, плейлисту и др.
- Добавлена десериализация `decomposed` у `Artist` ([#10](https://github.com/MarshalX/yandex-music-api/issues/10)).
- Добавлен `__len__` для `TracksList` ([#380](https://github.com/MarshalX/yandex-music-api/issues/380)).
- Добавлены `__iter__`, `__len__` и `__getitem__` для классов представляющих список каких-либо объектов.
- Добавлено сокращение `fetch_tracks` классу `Playlist` для получения треков плейлиста.
- Добавлен метод `get_url` классу `Icon` для получения прямой ссылки на изображение.
- Класс `User` расширен для поддержки поля `user_info` из `Track`(поля `full_name`, `display_name`).
- **Добавлены новые классы по отчётам с Telegram бота ([#306](https://github.com/MarshalX/yandex-music-api/issues/306), [#398](https://github.com/MarshalX/yandex-music-api/issues/398))**:
  - `LandingList`.
  - `RenewableRemainder`.
  - `Alert`.
  - `AlertButton`.
  - `StationData`.
  - `Brand`.
  - `Contest`.
  - `OpenGraphData`.
  - `NonAutoRenewable`.
  - `Operator`.
  - `Deactivation`.
  - `PoetryLoverMatch`.
  - `Deprecation`.
- **Добавлены новые поля классам по отчётам с Telegram бота ([#306](https://github.com/MarshalX/yandex-music-api/issues/306), [#398](https://github.com/MarshalX/yandex-music-api/issues/398))**:
  - `plus` в `Product`.
  - `non_auto_renewable_remainder` в `Subscription`.
  - `og_image` в `Artist`.
  - `meta_type` в `Album`.
  - `advertisement` в `Status`.
  - `best` в `Track`.
  - `offer_id` и `artist_ids` в `Vinyl`.
  - `playlists` в `BriefInfo`.
  - `is_custom` в `Cover`.
  - `play_count`, `recent`, `chart`, `track` в `TrackShort`.
  - `url_part`, `og_title`, `image`, `cover_without_text`, `background_color`, `text_color`, `id_for_from`,`similar_playlists`, `last_owner_playlists` в `Playlist`.
  - `bg_color` в `Chart`.
  - `error` в `Artist`.
  - `substituted`, `matched_track`, `can_publish`, `state`, `desired_visibility`, `filename`, `user_info`, `meta_data` в`Track`.
  - `copyright_name`, `copyright_cline` в `Cover`.
  - `direct` в `DownloadInfo`.
  - `cheapest`, `title`, `family_sub`, `fb_image`, `fb_name`,`family`, `intro_period_duration`, `intro_price`, `start_period_duration`, `start_price`, `licence_text_parts` в `Product`.
  - `storage_dir`, `duplicates` в `Album`.
  - `subscribed` в `ArtistEvent`.
  - `description` в `GeneratedPlaylist`.
  - `genre` в `Event`.
  - `show_in_regions` в `Genre`.
  - `cover_uri` в `MixLink`.
  - `og_description`, `top_artist` в `Playlist`.
  - `full_image_url`, `mts_full_image_url` в `Station`.
  - `coauthors` и `recent_tracks` в `Playlist`.
  - `regions` в `User`.
  - `users`, `podcasts`, `podcast_episodes`, `type_`, `page`, `per_page` в `Search`.
  - `short_description`, `description`, `is_premiere`, `is_banner` в `Like`.
  - `master_info` в `AutoRenewable`.
  - `station_data` и `bar_below` в `Status`.
  - `family_auto_renewable` в `Subscription`.
  - `misspell_result` и `misspell_original` в `Search`.
  - `experiment` в класс `Status`.
  - `operator` и `non_auto_renewable` в `Subscription`.
  - `text_color`, `short_description`, `description`, `is_premiere` и `is_banner` в `Album`.
  - `hand_made_description` в `Artist`.
  - `metrika_id` в `Playlist`.
  - `og_image` в `Tag`.
  - `url` в `Lyrics`.
  - `number`, `genre` в `MetaData`.
  - `poetry_lover_matches` в `Track`.
  - `contest`, `dummy_description`, `dummy_page_description`, `dummy_cover`, `dummy_rollover_cover`, `og_data`, `branding` в `Playlist`.
  - `available_as_rbt`, `lyrics_available`, `remember_position`, `albums`, `duration_ms`, `explicit`, `start_date`, `likes_count`, `deprecation` в `Album`.
  - `lyricist`, `version`, `composer` в `MetaData`.
  - `last_releases` в `BriefInfo`.
  - `ya_money_id` в `Artist` ([#351](https://github.com/MarshalX/yandex-music-api/issues/351), [#370](https://github.com/MarshalX/yandex-music-api/issues/370)).
  - `playlist_uuid` в `Playlist`.
  - `sync_queue_enabled` в `UserSettings`.
  - `background_video_uri`, `short_description`, `is_suitable_for_children` в `Track` ([#376](https://github.com/MarshalX/yandex-music-api/issues/376)).
  - `meta_type`, `likes_count` в `Album` ([#386](https://github.com/MarshalX/yandex-music-api/issues/386)).
  - `deprecation` в `Album`.
  - `available_regions` в `Album`.
  - `type`, `ready` в `Playlist`.
  - `description` в `Supplement`.

**Незначительные изменения и/или исправления**

- **Добавлена опциональность следующим полям**:
  - все поля в `MetaData`.
  - `advertisement` в `Status`.
  - `text_language` в `Lyrics`.
  - `provider_video_id` в `VideoSupplement`.
  - `title` в `VideoSupplement` ([#403](https://github.com/MarshalX/yandex-music-api/issues/403)).
  - `instructions` в `Deactivation` ([#402](https://github.com/MarshalX/yandex-music-api/issues/402)).
  - `id` в `Album` ([#401](https://github.com/MarshalX/yandex-music-api/issues/401)).

- Исправлена десериализация подкастов, эпизодов подкастов и пользователей в лучшем результате поиска.
- Исправлена десериализация альбомов. В зависимости от запроса содержимое лейблов может быть списком объектом или списком строк (в поиске).
- Исправлен выбор настроек радио.
- Исправлены ошибки в документации.
- Протестирована работа на Python 3.9.

## Версия 0.1.1

**25.03.2020**

**Закончено документирование всех классов и основных методов!**

**Переломные изменения**

- **Классы отметок "мне нравится" для альбомов, плейлистов и исполнителей обобщены. Теперь представлены одним классом**.
  - **Удаленные классы**:
    - `ArtistsLikes`.
    - `AlbumsLikes`.
    - `PlaylistsLikes`.
  - Новый класс: `Like` (поле `type` для определения содержимого).
- Изменено название пакета с `status` на `account` ([#195](https://github.com/MarshalX/yandex-music-api/issues/195)).
- **Исправлено выбрасываемое исключение при таймауте**:
  - Прошлое исключение: `TimeoutError` (built-in).
  - Новое исключение: `TimedOut` (`yandex_music.exceptions`).
- Удалены следующие файлы: `requirements.txt`, `requirements-dev.txt`,
  `requirements-docs.txt`.

**Крупные изменения**

- **Добавлено обнаружение новых полей с просьбой сообщить о них ([#216](https://github.com/MarshalX/yandex-music-api/issues/216))**.
  - Добавлена проверка на неизвестные поля.
  - Добавлен вывод отладочной информации в виде warning'a.
  - Добавлен шаблон issue для отправки логов.
- Добавлено поле `type` для класса `SearchResult` для определения типа результата поиска по объекту.
- **Добавлены настройки пользователя ([#195](https://github.com/MarshalX/yandex-music-api/issues/195))**:
  - Добавлен класс `UserSettings`.
  - Добавлен метод для получения своих настроек (`account_settings`).
  - Добавлен метод для получения настроек другого пользователя (`users_settings`).
  - Добавлен метод для изменения настроек (`account_settings_set`).
- **Добавлен возможность получить похожие треки ([#197](https://github.com/MarshalX/yandex-music-api/issues/197))**:
  - Добавлен класс `TracksSimilar` с полями трека и списка похожих треков.
  - Добавлен метод для получения похожих треков (`tracks_similar`).
- **Добавлены шоты от Алисы ([#185](https://github.com/MarshalX/yandex-music-api/issues/185))**:
  - Добавлен метод `after_track` в класс `Client` для получения контента для воспроизведения после трека (реклама, шот).
  - Добавлены методы для загрузки обложки и аудиоверсии шота.
  - **Добавлены новые классы**:
    - `Shot`
    - `ShotData`
    - `ShotEvent`
    - `ShotType`
- Добавлен метод для изменения видимости плейлиста ([#179](https://github.com/MarshalX/yandex-music-api/issues/179)).
- **Добавлена поддержка Яндекс.Радио ([#20](https://github.com/MarshalX/yandex-music-api/issues/20))**:
  - Исправлена отправка фидбека.
  - Написана инструкция по использованию (в доке к методу).
  - Добавлен аргумент для перехода по цепочке треков.
  - Добавлен метод для изменения настроек станции.

**Незначительные изменения и/или исправления**

- Убрано дублирование информации в документации ([#247](https://github.com/MarshalX/yandex-music-api/issues/247)).
- Добавлены новые поля в класс `Track`: `version`, `remember_position` ([#238](https://github.com/MarshalX/yandex-music-api/issues/238)).
- Добавлено исключение `InvalidBitrate` при попытке загрузить недопустимый трек по критериям (кодек, битрейт).
- Исправлено получение прямой ссылки на файл с кодеком AAC ([#237](https://github.com/MarshalX/yandex-music-api/issues/237), [#25](https://github.com/MarshalX/yandex-music-api/issues/25)).
- Исправлено получение плейлиста с Алисой в лендинге ([#185](https://github.com/MarshalX/yandex-music-api/issues/185)).
- Исправлено название поля с ссылкой на источник в классе `Description` (с `url` на `uri`).
- Исправлена десериализация несуществующего исполнителя.
- Добавлено поле `version` в класс `Album` ([#178](https://github.com/MarshalX/yandex-music-api/issues/178)).
- Поле `picture` класса `Vinyl` теперь опциональное.
- Поле `week` класса `Ratings` теперь опциональное.
- Поле `product_id` класса `AutoRenewable` теперь опциональное ([#182](https://github.com/MarshalX/yandex-music-api/issues/182)).
- Правки замечаний по codacy.

## Версия 0.0.16

**29.12.2019**

**Переломные изменения**

- Поле `account` переименовано в `me` и теперь содержит объект `Status`, вместо `Account` ([#162](https://github.com/MarshalX/yandex-music-api/issues/162)).
- Убрано использование зарезервированных имён в аргументах конструкторов (теперь они с `_` на конце). Имена с нижними подчёркиваниями есть как при сериализации так и при десериализации ([#168](https://github.com/MarshalX/yandex-music-api/issues/168)).

**Крупные изменения**

- **Добавлены аннотации типов во всей библиотеке!**

**Незначительные изменения и/или исправления**

- Добавлен аргумент `fetch_account_status` для опциональности получения информации об аккаунте при инициализации клиента ([#162](https://github.com/MarshalX/yandex-music-api/issues/162)).
- Добавлены тесты c передачей пустого словаря в `de_json` и `de_list` ([#174](https://github.com/MarshalX/yandex-music-api/issues/174)).
- Использование `ujson` при наличии, обновлены зависимости ([#161](https://github.com/MarshalX/yandex-music-api/issues/161)).
- Добавлен в зависимости для разработки `importlib_metadata` для  поддержки старых версий (в новой версии `pytest` его больше не используют, в угоду `importlib.metadata` [#pytest-5537](https://github.com/pytest-dev/pytest/issues/5537))) ([#161](https://github.com/MarshalX/yandex-music-api/issues/161)).
- Добавлен в зависимости для разработки `atomicwrites`, который используется `pytest` теперь только на `Windows` - [#pytest-6148](https://github.com/pytest-dev/pytest/pull/6148) ([#161](https://github.com/MarshalX/yandex-music-api/issues/161)).
- Исправлен баг с передачей `timeout` аргумента в аргумент `params` в следующих методах: `artists`, `albums`, `playlists_list` ([#120](https://github.com/MarshalX/yandex-music-api/issues/120)).
- Исправлена инициализация клиента при помощи логина и пароля с использованием прокси ([#159](https://github.com/MarshalX/yandex-music-api/issues/159)).
- Исправлен баг в загрузке обложки альбома.

## Версия 0.0.15

**01.12.2019**

**Переломные изменения**

- У классов `Artist`, `Track` и `Playlist` изменился перечень полей для генерации хеша.

**Крупные изменения**

- **Добавлена возможность выполнять запросы через прокси-сервер для использовании библиотеки на зарубежных серверах ([#139](https://github.com/MarshalX/yandex-music-api/issues/139))**.
  - Добавлен пример использования в `README`.
- **Добавлена обработка капчи при авторизации с возможностью использования callback-функции для её обработки ([#140](https://github.com/MarshalX/yandex-music-api/issues/140))**:
  - **Новые исключения**:
    - **Captcha**:
      - CaptchaRequired.
      - CaptchaWrong.
  - **Новые классы**:
    - CaptchaResponse.
  - **Новые примеры в `README`**:
    - Пример обработки с использованием callback-функции.
    - Пример полностью своей обработки капчи.
- Добавлена документация для класса `Search` ([#83](https://github.com/MarshalX/yandex-music-api/issues/83)).
- **Добавлена возможность получения всех альбомов исполнителя ([#141](https://github.com/MarshalX/yandex-music-api/issues/141))**:
  - **Новые классы**:
    - ArtistAlbums.
  - **Новые методы**:
    - `artists_direct_albums` у `Client`.
    - `get_albums` у `Artist`.
- **Добавлена обработка несуществующего плейлиста ([#147](https://github.com/MarshalX/yandex-music-api/issues/147))**:
  - **Новые классы**:
    - `PlaylistAbsence`.

**Незначительные изменения и/или исправления**

- Исправлен баг с загрузкой файлов ([#149](https://github.com/MarshalX/yandex-music-api/issues/149)).
- Исправлен баг некорректной десериализации плейлиста при отсутствии прав на него ([#147](https://github.com/MarshalX/yandex-music-api/issues/147)).
- Исправлен баг неправильной десериализации треков и артистов у собственных загруженных файлов ([#154](https://github.com/MarshalX/yandex-music-api/issues/154)).

## Версия 0.0.14

**10.11.2019**

**Переломные изменения**

- Практически у всех классов был обновлён список полей участвующих при сравнении объектов.
- Если в атрибутах для сравнения объектов присутствуют списки, то они будут преобразованы к frozenset.
- Убрано конвертирование даты из строки в объект. Теперь все даты представлены строками в ISO формате.
- Классы `AlbumSearchResult`, `ArtistSearchResult`, `PlaylistSearchResult`, `TrackSearchResult`, `VideoSearchResult` были объединены в один – `SearchResult`.

**Крупные изменения**

- Добавлен метод получения треков исполнителя ([#123](https://github.com/MarshalX/yandex-music-api/pull/123)).
- Добавлены классы-обёртки над пагинацией (`Pager`) и списка треков артиста (`ArtistsTracks`).
- Добавлено **554** unit-теста для всех классов-обёрток над объектами API.
- Добавлен codecov и workflows для GitHub Actions.

**Незначительные изменения и/или исправления**

- Поле `cover_uri` класса `Album` теперь опциональное.
- Поле `region` у класса `Account` теперь не обязательное.
- Исправлен баг в `.to_dict()` методе, связанный с десериализацией объектов списков и словарей.
- Исправлен баг в `.to_dict()` методе, связанный с не рекурсивной десериализацией.
- Исправлена десериализация `similar_artists` в `BriefInfo`.
- Исправлен баг с десериализацией `artist` в классе `ArtistEvent`.
- Исправлен баг десериализации списка альбомов и артистов у класса `Track` ([#122](https://github.com/MarshalX/yandex-music-api/pull/122)).
- Исправлена загрузка обложки у трека.
- Исправлены сравнения объектов.
