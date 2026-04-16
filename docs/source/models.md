# Модели

Объекты API Яндекс Музыки, возвращаемые методами клиента, представлены dataclass-моделями. Каждая модель наследуется от {class}`yandex_music.base.YandexMusicModel` и поддерживает:

- `from_json(data, client)` — десериализация из JSON-ответа API.
- `to_dict()` / `to_json()` — обратное преобразование.
- Lazy-методы, обращающиеся к клиенту (например, `Track.download(...)` вызывает `Client.tracks_download_info(...)` с `track.id`).

Модели сгруппированы по доменам. Базовые конструкции (`YandexMusicModel`, `YandexMusicObject`, JSON-типы) — на странице {doc}`Базовые классы <yandex_music.base>`.

## Каталог

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`play;1em;sd-mr-1` Трек
      :link: yandex_music.track
      :link-type: doc

      Треки, лирика, варианты, трейлеры.

   .. grid-item-card:: :octicon:`package;1em;sd-mr-1` Альбом
      :link: yandex_music.album
      :link-type: doc

      Альбомы, трейлеры, кнопки действий, похожие альбомы.

   .. grid-item-card:: :octicon:`person;1em;sd-mr-1` Артист
      :link: yandex_music.artist
      :link-type: doc

      Артисты, биография, клипы, донаты, трейлеры, похожие.

   .. grid-item-card:: :octicon:`list-unordered;1em;sd-mr-1` Плейлист
      :link: yandex_music.playlist
      :link-type: doc

      Плейлисты пользователей и редакторские, рекомендации, теги.

   .. grid-item-card:: :octicon:`tag;1em;sd-mr-1` Лейбл
      :link: yandex_music.label
      :link-type: doc

      Лейблы, их альбомы и артисты.

   .. grid-item-card:: :octicon:`hash;1em;sd-mr-1` Жанры
      :link: yandex_music.genre
      :link-type: doc

      Справочник жанров с изображениями.
```

## Поиск и подборки

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`search;1em;sd-mr-1` Поиск
      :link: yandex_music.search
      :link-type: doc

      Результаты поиска, подсказки, лучшие совпадения.

   .. grid-item-card:: :octicon:`filter;1em;sd-mr-1` Метатеги
      :link: yandex_music.metatag
      :link-type: doc

      Жанры/настроения/эпохи для фильтрации контента.

   .. grid-item-card:: :octicon:`home;1em;sd-mr-1` Лендинг
      :link: yandex_music.landing
      :link-type: doc

      Главный экран: блоки, чарты, промо, рекомендации.

   .. grid-item-card:: :octicon:`rss;1em;sd-mr-1` Лента
      :link: yandex_music.feed
      :link-type: doc

      События пользователя: новые релизы, ежедневные плейлисты.
```

## Радио и волна

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`broadcast;1em;sd-mr-1` Радио
      :link: yandex_music.rotor
      :link-type: doc

      Rotor: станции, дашборд, настройки, последовательности.

   .. grid-item-card:: :octicon:`pulse;1em;sd-mr-1` Волна
      :link: yandex_music.wave
      :link-type: doc

      Персональная волна и связанные сущности.
```

## Пользователь и аккаунт

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`person-fill;1em;sd-mr-1` Аккаунт
      :link: yandex_music.account
      :link-type: doc

      Статус, подписка, права, алерты.

   .. grid-item-card:: :octicon:`heart;1em;sd-mr-1` Лайки
      :link: yandex_music.like
      :link-type: doc

      Объекты лайков на треки/артистов/альбомы.

   .. grid-item-card:: :octicon:`list-ordered;1em;sd-mr-1` Очередь
      :link: yandex_music.queue
      :link-type: doc

      Очередь воспроизведения и её контекст.

   .. grid-item-card:: :octicon:`history;1em;sd-mr-1` История
      :link: yandex_music.music_history
      :link-type: doc

      История прослушивания с группировкой.

   .. grid-item-card:: :octicon:`pin;1em;sd-mr-1` Закреплённые
      :link: yandex_music.pin
      :link-type: doc

      Закреплённые в библиотеке элементы.

   .. grid-item-card:: :octicon:`bookmark;1em;sd-mr-1` Пресейвы
      :link: yandex_music.presave
      :link-type: doc

      Предсохранения альбомов.

   .. grid-item-card:: :octicon:`beaker;1em;sd-mr-1` Эксперименты
      :link: yandex_music.experiment
      :link-type: doc

      A/B-эксперименты аккаунта и их параметры.

   .. grid-item-card:: :octicon:`beaker;1em;sd-mr-1` Experiments (legacy)
      :link: yandex_music.experiments
      :link-type: doc

      Легаси-контейнер флагов экспериментальных функций.
```

## Креатив и агрегаты

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`video;1em;sd-mr-1` Клипы
      :link: yandex_music.clip
      :link-type: doc

      Видео-клипы артистов и треков.

   .. grid-item-card:: :octicon:`calendar;1em;sd-mr-1` Концерты
      :link: yandex_music.concert
      :link-type: doc

      Концерты и связанные сущности.

   .. grid-item-card:: :octicon:`info;1em;sd-mr-1` Доп. информация
      :link: yandex_music.supplement
      :link-type: doc

      Лирика, видео, описания.

   .. grid-item-card:: :octicon:`people;1em;sd-mr-1` Credits
      :link: yandex_music.credits
      :link-type: doc

      Участники создания трека.

   .. grid-item-card:: :octicon:`person;1em;sd-mr-1` Credit (одиночный)
      :link: yandex_music.credit
      :link-type: doc

      Запись одного участника.

   .. grid-item-card:: :octicon:`megaphone;1em;sd-mr-1` Шоты
      :link: yandex_music.shot
      :link-type: doc

      Голосовые врезки ведущего.

   .. grid-item-card:: :octicon:`browser;1em;sd-mr-1` Скелетоны
      :link: yandex_music.skeleton
      :link-type: doc

      Плейсхолдеры UI.

   .. grid-item-card:: :octicon:`play;1em;sd-mr-1` Трейлеры
      :link: yandex_music.trailer_info
      :link-type: doc

      Обёртка над разными типами трейлеров.
```

## Прочее

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`alert;1em;sd-mr-1` Дисклеймер
      :link: yandex_music.disclaimer
      :link-type: doc

      Дисклеймеры контента.

   .. grid-item-card:: :octicon:`device-camera-video;1em;sd-mr-1` Видео
      :link: yandex_music.video
      :link-type: doc

      Видео-объекты.

   .. grid-item-card:: :octicon:`image;1em;sd-mr-1` Обложка
      :link: yandex_music.cover
      :link-type: doc

      Обложки альбомов/плейлистов/артистов.

   .. grid-item-card:: :octicon:`paintbrush;1em;sd-mr-1` Цвета обложки
      :link: yandex_music.cover_derived_colors
      :link-type: doc

      Палитры, выведенные из обложки.

   .. grid-item-card:: :octicon:`download;1em;sd-mr-1` Скачивание
      :link: yandex_music.download_info
      :link-type: doc

      Информация для загрузки медиа.

   .. grid-item-card:: :octicon:`number;1em;sd-mr-1` Пагинация
      :link: yandex_music.pager
      :link-type: doc

      Общий пагинатор ответов API.

   .. grid-item-card:: :octicon:`shield;1em;sd-mr-1` Content Restrictions
      :link: yandex_music.content_restrictions
      :link-type: doc

      Ограничения контента по региону/возрасту.

   .. grid-item-card:: :octicon:`report;1em;sd-mr-1` Foreign Agent
      :link: yandex_music.foreign_agent
      :link-type: doc

      Маркировка иностранного агента.

   .. grid-item-card:: :octicon:`apps;1em;sd-mr-1` Иконка
      :link: yandex_music.icon
      :link-type: doc

      Иконка сущности.

   .. grid-item-card:: :octicon:`telescope;1em;sd-mr-1` Invocation Info
      :link: yandex_music.invocation_info
      :link-type: doc

      Метаданные вызова API.

   .. grid-item-card:: :octicon:`shield-lock;1em;sd-mr-1` Permission Alerts
      :link: yandex_music.permission_alerts
      :link-type: doc

      Оповещения о правах.

   .. grid-item-card:: :octicon:`key;1em;sd-mr-1` Promo Code Status
      :link: yandex_music.promo_code_status
      :link-type: doc

      Статус активации промокода.

   .. grid-item-card:: :octicon:`gear;1em;sd-mr-1` Settings
      :link: yandex_music.settings
      :link-type: doc

      Настройки приложения/аккаунта.

   .. grid-item-card:: :octicon:`file-media;1em;sd-mr-1` Track Short
      :link: yandex_music.track_short
      :link-type: doc

      Облегчённая ссылка на трек.

   .. grid-item-card:: :octicon:`list-unordered;1em;sd-mr-1` Tracks List
      :link: yandex_music.tracks_list
      :link-type: doc

      Список облегчённых ссылок.
```

<!-- generated-models-toctree -->

```{eval-rst}
.. toctree::
   :hidden:
   :maxdepth: 2

   yandex_music.account
   yandex_music.album
   yandex_music.artist
   yandex_music.clip
   yandex_music.concert
   yandex_music.experiment
   yandex_music.feed
   yandex_music.genre
   yandex_music.label
   yandex_music.landing
   yandex_music.metatag
   yandex_music.music_history
   yandex_music.pin
   yandex_music.playlist
   yandex_music.presave
   yandex_music.queue
   yandex_music.rotor
   yandex_music.search
   yandex_music.shot
   yandex_music.skeleton
   yandex_music.supplement
   yandex_music.track
   yandex_music.wave
   yandex_music.content_restrictions
   yandex_music.cover
   yandex_music.cover_derived_colors
   yandex_music.credit
   yandex_music.credits
   yandex_music.disclaimer
   yandex_music.download_info
   yandex_music.experiments
   yandex_music.foreign_agent
   yandex_music.icon
   yandex_music.invocation_info
   yandex_music.like
   yandex_music.pager
   yandex_music.permission_alerts
   yandex_music.promo_code_status
   yandex_music.settings
   yandex_music.track_short
   yandex_music.tracks_list
   yandex_music.trailer_info
   yandex_music.video
```
