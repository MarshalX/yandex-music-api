================
Список изменений
================

Версия 1.0.0
============

**XX.02.2021**

**Стабильная версия библиотеки**

**Переломные изменения**

- Поле ``error`` класса ``Artist`` теперь называется ``reason``.
- Метод ``users_playlists`` класса ``Client`` теперь возвращает один объект плейлиста, когда был передан один ``kind``. При передаче списка в ``kind`` вернётся список плейлистов (`#318`_).
- Поле ``labels`` класса ``Album`` теперь может содержать список из строк, а не только список объектов класса ``Label``.

**Крупные изменения**

- Добавлены примеры в папку ``examples``.
- Новые поля и классы по первым отчётам `#306`_:
    - Добавлен класс ``RenewableRemainder`` напоминал о продлении подписки.
    - Добавлено поле ``plus`` класса ``Product``.
    - Добавлено поле ``non_auto_renewable_remainder`` в класс ``Subscription`` с новым классом.
    - Добавлено поле ``og_image`` классу ``Artist``.
    - Добавлено поле ``meta_type`` классу ``Album``.
    - Добавлено поле ``advertisement`` классу ``Status``.
    - Добавлено поле ``best`` классу ``Track``.
    - Добавлены поля ``offer_id`` и ``artist_ids`` классу ``Vinyl``.
    - Добавлено поле ``playlists`` классу ``BriefInfo``.
    - Добавлено поле ``is_custom`` классу ``Cover``.
- Добавлена поддержка рекомендаций для плейлистов (`#324`_):
    - Добавлен класс ``PlaylistRecommendations``.
    - Добавлен метод клиента для получения рекомендаций (``users_playlists_recommendations``).
    - Добавлен метод ``get_recommendations`` классу ``Playlist`` для получения рекомендаций.
- Добавлено получение чартов (`#294`_):
    - Добавлены новые классы: ``ChartInfo``, ``ChartInfoMenu``, ``ChartInfoMenuItem``.
    - Добавлен метод клиента для получения чарта (``chart``).
- Добавлена поддержка тегов/подборок (`#192`_):
    - Добавлены новые классы: ``TagResult``, ``Tag``
    - Добавлен новый метод клиента для получения тегов (``tags``).
- Добавлено присоединение к коллективному плейлисту (`#317`_):
    - Добавлен новый метод клиента для присоединения (``playlists_collective_join``).
- Добавлено сокращение ``fetch_tracks`` классу ``Playlist`` для получения треков плейлиста.
- Добавлены поля ``play_count``, ``recent``, ``chart``, ``track`` классу ``TrackShort``.
- Добавлены поля ``url_part``, ``og_title``, ``image``, ``cover_without_text``, ``background_color``, ``text_color``, ``id_for_from``, ``similar_playlists``, ``last_owner_playlists`` классу ``Playlist``.
- Добавлено поле ``bg_color`` классу ``Chart``.
- Добавлен новый класс ``LandingList``.
- Добавлен новый метод клиента для получения полного списка всех новых релизов (``new_releases``).
- Добавлен новый метод клиента для получения полного списка всех новый плейлистов (``new_playlists``).
- Добавлен новый метод клиента для получения подкаста с лендинга (``podcasts``).
- Добавлено поле ``error`` классу ``Artist``.
- Класс ``User`` расширен для поддержки поля ``user_info`` из ``Track`` (поля ``full_name``, ``display_name``).
- Добавлены новые поля классу ``Track``: ``substituted``, ``matched_track``, ``can_publish``, ``state``, ``desired_visibility``, ``filename``, ``user_info``, ``meta_data``.
- Добавлены новые поля класса ``Cover``: ``copyright_name``, ``copyright_cline``.
- Добавлено поле ``direct`` классу ``DownloadInfo``.
- Добавлены поля ``cheapest``, ``title``, ``family_sub``, ``fb_image``, ``fb_name``, ``family``, ``intro_period_duration``, ``intro_price``, ``start_period_duration``, ``start_price``, ``licence_text_parts`` для ``Product``.
- Добавлены поля ``storage_dir``, ``duplicates`` для ``Album``.
- Добавлено поле ``subscribed`` для ``ArtistEvent``.
- Добавлено поле ``description`` для ``GeneratedPlaylist``.
- Добавлено поле ``genre`` для ``Event``.
- Добавлено поле ``show_in_regions`` для ``Genre``.
- Добавлено поле ``cover_uri`` для ``MixLink``.
- Добавлены поля ``og_description``, ``top_artist`` для ``Playlist``.
- Добавлены поля ``full_image_url``, ``mts_full_image_url`` для ``Station``.
- Добавлены поля ``coauthors`` и ``recent_tracks`` в ``Playlist``.
- Добавлено поле ``regions`` в ``User``.
- Добавлены поля ``users``, ``podcasts``, ``podcast_episodes``, ``type_``, ``page``, ``per_page`` в ``Search``.
- Добавлена поддержка новых типов поиска: подкасты, выпуски, пользователи.
- Добавлены поля ``short_description``, ``description``, ``is_premiere``, ``is_banner`` в ``Like``.
- Добавлены новые классы: ``Alert``, ``AlertButton``, ``StationData``.
- Добавлено поле ``master_info`` в ``AutoRenewable``.
- Добавлены поля ``station_data`` и ``bar_below`` в ``Status``.
- Добавлено поле ``family_auto_renewable`` в ``Subscription``.
- Добавлены поля ``misspell_result`` и ``misspell_original`` в ``Search``.
- Добавлена десериализация ``decomposed`` у ``Artist`` (`#10`_).
- Добавлено новое поле ``experiment`` в класс ``Status``.
- Добавлен коллбек для обработки новых полей.
- Добавлены новые классы: ``NonAutoRenewable``, ``Operator``, ``Deactivation``, ``PoetryLoverMatch``.
- Добавлены поля ``operator`` и ``non_auto_renewable`` в ``Subscription``.
- Добавлены поля ``text_color``, ``short_description``, ``description``, ``is_premiere`` и ``is_banner`` в ``Album``.
- Добавлено поле ``hand_made_description`` в ``Artist``.
- Добавлено поле ``metrika_id`` в ``Playlist``.
- Добавлено поле ``og_image`` в ``Tag``.
- Добавлено поле url в ``Lyrics``.
- Добавлены поля ``number``, ``genre`` в ``MetaData``.
- Добавлено поле ``poetry_lover_matches`` в ``Track``.
- Добавлены новые классы: ``Brand``, ``Contest``, ``OpenGraphData``.
- Добавлены поля ``contest``, ``dummy_description``, ``dummy_page_description``, ``dummy_cover``, ``dummy_rollover_cover``, ``og_data``, ``branding`` классу ``Playlist``.
- Добавлена информацию по поводу запуска потока по треку, плейлисту и др.
- Добавлена поддержка очередей прослушивания (`#246`_):
    - Добавлены новые классы: ``Context``, ``Queue``, ``QueueItem``.
    - Добавлены новые методы в ``Client``: ``queues_list``, ``queue``, ``queue_update_position``, ``queue_create``.
    - Добавлены поля ``track_id`` и ``from_`` в класс ``TrackId``.
    - Добавлена возможность смены языка у клиента для ответов от API.
    - Добавлена десериализация любого объекта в ``JSON`` пригодного для отправки в запросе на Яндекс API.
- Добавлен метод ``get_url`` классу ``Icon`` для получения прямой ссылки на изображение.
- Добавлен ``__len__`` для ``TracksList`` (`#380`_).
- Добавлены новые поля класса ``Album`` (``available_as_rbt``, ``lyrics_available``, ``remember_position``, ``albums``, ``duration_ms``, ``explicit``, ``start_date``, ``likes_count``, ``deprecation``).
- Добавлены новые поля класса ``MetaData`` (``lyricist``, ``version``, ``composer``).
- Добавлены поле ``last_releases`` классу ``BriefInfo``.
- Добавлено поле ``ya_money_id`` классу ``Artist`` (`#351`_, `#370`_).
- Добавлено поле ``playlist_uuid`` классу ``Playlist``.
- Добавлены поля и обновлены тесты для класса ``UserSettings``.
- Добавлены поля ``background_video_uri``, ``short_description``, ``is_suitable_for_children`` классу ``Track`` (`#376`_).
- Добавлены новые поля ``meta_type``, ``likes_count`` классу ``Album`` (`#386`_).
- Добавлен новый класс ``Deprecation``.
- Добавлено поле ``deprecation`` для класса ``Album``.
- Добавлено новое поле ``available_regions`` для ``Album``.
- Добавлены ``__iter__``, ``__len__`` и ``__getitem__`` для классов представляющих список каких-либо объектов.

**Незначительные изменения и/или исправления**

- Исправлена десериализация подкастов, эпизодов подкастов и пользователей в лучшем результате поиска.
- Исправлена десериализация альбомов. В зависимости от запроса содержимое лейблов может быть списком объектом или списком строк.
- Все поля класса ``MetaData`` теперь опциональные.
- Исправлен выбор настроек радио.
- Протестирована работа на Python 3.9.
- Поле ``advertisement`` класса ``Status`` теперь опциональное.
- Поле ``text_language`` класса ``Lyrics`` и ``provider_video_id`` класса ``VideoSupplement`` теперь опциональные.
- Исправлены ошибки в документации.

.. _`#318`: https://github.com/MarshalX/yandex-music-api/issues/318
.. _`#306`: https://github.com/MarshalX/yandex-music-api/issues/306
.. _`#324`: https://github.com/MarshalX/yandex-music-api/issues/324
.. _`#294`: https://github.com/MarshalX/yandex-music-api/issues/294
.. _`#192`: https://github.com/MarshalX/yandex-music-api/issues/192
.. _`#317`: https://github.com/MarshalX/yandex-music-api/issues/317
.. _`#10`: https://github.com/MarshalX/yandex-music-api/issues/10
.. _`#386`: https://github.com/MarshalX/yandex-music-api/issues/386
.. _`#246`: https://github.com/MarshalX/yandex-music-api/issues/246
.. _`#376`: https://github.com/MarshalX/yandex-music-api/issues/376
.. _`#351`: https://github.com/MarshalX/yandex-music-api/issues/351
.. _`#370`: https://github.com/MarshalX/yandex-music-api/issues/370
.. _`#380`: https://github.com/MarshalX/yandex-music-api/issues/380

Версия 0.1.1
============

**25.03.2020**

**Закончено документирование всех классов и основных методов!**

**Переломные изменения**

- Классы отметок "мне нравится" для альбомов, плейлистов и исполнителей обобщены. Теперь представлены одним классом.
    - Удаленные классы:
        - ``ArtistsLikes``.
        - ``AlbumsLikes``.
        - ``PlaylistsLikes``.
    - Новый класс: ``Like`` (поле ``type`` для определения содержимого).
- Изменено название пакета с ``status`` на ``account`` (`#195`_).
- Исправлено выбрасываемое исключение при таймауте:
    - Прошлое исключение: ``TimeoutError`` (built-in).
    - Новое исключение: ``TimedOut`` (``yandex_music.exceptions``).
- Удалены следующие файлы: ``requirements.txt``, ``requirements-dev.txt``, ``requirements-docs.txt``.

**Крупные изменения**

- Добавлено обнаружение новых полей с просьбой сообщить о них (`#216`_).
    - Добавлена проверка на неизвестные поля.
    - Добавлен вывод отладочной информации в виде warning'a.
    - Добавлен шаблон issue для отправки логов.
- Добавлено поле ``type`` для класса ``SearchResult`` для определения типа результата поиска по объекту.
- Добавлены настройки пользователя (`#195`_):
    - Добавлен класс ``UserSettings``.
    - Добавлен метод для получения своих настроек (``account_settings``).
    - Добавлен метод для получения настроек другого пользователя (``users_settings``).
    - Добавлен метод для изменения настроек (``account_settings_set``).
- Добавлен возможность получить похожие треки (`#197`_):
    - Добавлен класс ``TracksSimilar`` с полями трека и списка похожих треков.
    - Добавлен метод для получения похожих треков (``tracks_similar``).
- Добавлены шоты от Алисы (`#185`_):
    - Добавлен метод ``after_track`` в класс ``Client`` для получения контента для воспроизведения после трека (реклама, шот).
    - Добавлены методы для загрузки обложки и аудиоверсии шота.
    - Добавлены новые классы:
        - ``Shot``
        - ``ShotData``
        - ``ShotEvent``
        - ``ShotType``
- Добавлен метод для изменения видимости плейлиста (`#179`_).
- Добавлена поддержка Яндекс.Радио (`#20`_):
    - Исправлена отправка фидбека.
    - Написана инструкция по использованию (в доке к методу).
    - Добавлен аргумент для перехода по цепочке треков.
    - Добавлен метод для изменения настроек станции.

**Незначительные изменения и/или исправления**

- Убрано дублирование информации в документации (`#247`_).
- Добавлены новые поля в класс ``Track``: ``version``, ``remember_position`` (`#238`_).
- Добавлено исключение ``InvalidBitrate`` при попытке загрузить недопустимый трек по критериям (кодек, битрейт).
- Исправлено получение прямой ссылки на файл с кодеком AAC (`#237`_, `#25`_).
- Исправлено получение плейлиста с Алисой в лендинге (`#185`_).
- Исправлено название поля с ссылкой на источник в классе ``Description`` (с ``url`` на ``uri``).
- Исправлена десериализация несуществующего исполнителя.
- Добавлено поле ``version`` в класс ``Album`` (`#178`_).
- Поле ``picture`` класса ``Vinyl`` теперь опциональное.
- Поле ``week`` класса ``Ratings`` теперь опциональное.
- Поле ``product_id`` класса ``AutoRenewable`` теперь опциональное (`#182`_).
- Правки замечаний по codacy.

.. _`#216`: https://github.com/MarshalX/yandex-music-api/issues/216
.. _`#247`: https://github.com/MarshalX/yandex-music-api/issues/247
.. _`#237`: https://github.com/MarshalX/yandex-music-api/issues/237
.. _`#25`: https://github.com/MarshalX/yandex-music-api/issues/25
.. _`#238`: https://github.com/MarshalX/yandex-music-api/issues/238
.. _`#182`: https://github.com/MarshalX/yandex-music-api/issues/182
.. _`#195`: https://github.com/MarshalX/yandex-music-api/issues/195
.. _`#197`: https://github.com/MarshalX/yandex-music-api/issues/197
.. _`#20`: https://github.com/MarshalX/yandex-music-api/issues/20
.. _`#185`: https://github.com/MarshalX/yandex-music-api/issues/185
.. _`#179`: https://github.com/MarshalX/yandex-music-api/issues/179
.. _`#178`: https://github.com/MarshalX/yandex-music-api/issues/178

Версия 0.0.16
=============

**29.12.2019**

**Переломные изменения**

- Поле ``account`` переименовано в ``me`` и теперь содержит объект ``Status``, вместо ``Account`` (`#162`_).
- Убрано использование зарезервированных имён в аргументах конструкторов (теперь они с ``_`` на конце). Имена с нижними подчёркиваниями есть как при сериализации так и при десериализации (`#168`_).

**Крупные изменения**

- **Добавлены аннотации типов во всей библиотеке!**

**Незначительные изменения и/или исправления**

- Добавлен аргумент ``fetch_account_status`` для опциональности получения информации об аккаунте при инициализации клиента (`#162`_).
- Добавлены тесты c передачей пустого словаря в ``de_json`` и ``de_list`` (`#174`_).
- Использование ``ujson`` при наличии, обновлены зависимости (`#161`_).
- Добавлен в зависимости для разработки ``importlib_metadata`` для поддержки старых версий (в новой версии ``pytest`` его больше не используют, в угоду ``importlib.metadata`` `#pytest-5537`_)) (`#161`_).
- Добавлен в зависимости для разработки ``atomicwrites``, который используется ``pytest`` теперь только на ``Windows`` - `#pytest-6148`_ (`#161`_).
- Исправлен баг с передачей ``timeout`` аргумента в аргумент ``params`` в следующих методах: ``artists``, ``albums``, ``playlists_list`` (`#120`_).
- Исправлена инициализация клиента при помощи логина и пароля с использованием прокси (`#159`_).
- Исправлен баг в загрузке обложки альбома.

.. _`#162`: https://github.com/MarshalX/yandex-music-api/issues/162
.. _`#161`: https://github.com/MarshalX/yandex-music-api/issues/161
.. _`#159`: https://github.com/MarshalX/yandex-music-api/issues/159
.. _`#168`: https://github.com/MarshalX/yandex-music-api/issues/168
.. _`#120`: https://github.com/MarshalX/yandex-music-api/issues/120
.. _`#174`: https://github.com/MarshalX/yandex-music-api/issues/174
.. _`#pytest-5537`: https://github.com/pytest-dev/pytest/issues/5537
.. _`#pytest-6148`: https://github.com/pytest-dev/pytest/pull/6148

Версия 0.0.15
=============

**01.12.2019**

**Переломные изменения**

- У классов ``Artist``, ``Track`` и ``Playlist`` изменился перечень полей для генерации хеша.

**Крупные изменения**

- Добавлена возможность выполнять запросы через прокси-сервер для использовании библиотеки на зарубежных серверах (`#139`_).
    - Добавлен пример использования в ``README``.
- Добавлена обработка капчи при авторизации с возможностью использования callback-функции для её обработки (`#140`_):
    - Новые исключения:
        - Captcha:
            - CaptchaRequired.
            - CaptchaWrong.
    - Новые классы:
        - CaptchaResponse.
    - Новые примеры в ``README``:
        - Пример обработки с использованием callback-функции.
        - Пример полностью своей обработки капчи.
- Добавлена документация для класса ``Search`` (`#83`_).
- Добавлена возможность получения всех альбомов исполнителя (`#141`_):
    - Новые классы:
        - ArtistAlbums.
    - Новые методы:
        - ``artists_direct_albums`` у ``Client``.
        - ``get_albums`` у ``Artist``.
- Добавлена обработка несуществующего плейлиста (`#147`_):
    - Новые классы:
        - ``PlaylistAbsence``.

**Незначительные изменения и/или исправления**

- Исправлен баг с загрузкой файлов (`#149`_).
- Исправлен баг некорректной десериализации плейлиста при отсутствии прав на него (`#147`_).
- Исправлен баг неправильной десериализации треков и артистов у собственных загруженных файлов (`#154`_).

.. _`#139`: https://github.com/MarshalX/yandex-music-api/issues/139
.. _`#140`: https://github.com/MarshalX/yandex-music-api/issues/140
.. _`#83`: https://github.com/MarshalX/yandex-music-api/issues/83
.. _`#141`: https://github.com/MarshalX/yandex-music-api/issues/141
.. _`#149`: https://github.com/MarshalX/yandex-music-api/issues/149
.. _`#147`: https://github.com/MarshalX/yandex-music-api/issues/147
.. _`#154`: https://github.com/MarshalX/yandex-music-api/issues/154

Версия 0.0.14
=============

**10.11.2019**

**Переломные изменения**

- Практически у всех классов был обновлён список полей участвующих при сравнении объектов.
- Если в атрибутах для сравнения объектов присутствуют списки, то они будут преобразованы к frozenset.
- Убрано конвертирование даты из строки в объект. Теперь все даты представлены строками в ISO формате.
- Классы ``AlbumSearchResult``, ``ArtistSearchResult``, ``PlaylistSearchResult``, ``TrackSearchResult``, ``VideoSearchResult`` были объединены в один - ``SearchResult``.

**Крупные изменения**

- Добавлен метод получения треков исполнителя (`#123`_).
- Добавлены классы-обёртки над пагинацией (``Pager``) и списка треков артиста (``ArtistsTracks``).
- Добавлено **554** unit-теста для всех классов-обёрток над объектами API.
- Добавлен codecov и workflows для GitHub Actions.

.. _`#123`: https://github.com/MarshalX/yandex-music-api/pull/123

**Незначительные изменения и/или исправления**

- Поле ``cover_uri`` класса ``Album`` теперь опциональное.
- Поле ``region`` у класса ``Account`` теперь не обязательное.
- Исправлен баг в ``.to_dict()`` методе, связанный с десериализцией объектов списков и словарей.
- Исправлен баг в ``.to_dict()`` методе, связанный с не рекурсивной десериализацией.
- Исправлена десериализация ``similar_artists`` в ``BriefInfo``.
- Исправлен баг с десериализацией ``artist`` в классе ``ArtistEvent``.
- Исправлен баг десериализации списка альбомов и артистов у класса ``Track`` (`#122`_).
- Исправлена загрузка обложки у трека.
- Исправлены сравнения объектов.

.. _`#122`: https://github.com/MarshalX/yandex-music-api/pull/122
