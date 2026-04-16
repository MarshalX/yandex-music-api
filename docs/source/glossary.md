# Глоссарий

Термины и сущности API Яндекс Музыки, встречающиеся в документации моделей и методов клиента. Ссылка на термин в docstring'ах — `` :term:`<name>` ``.

```{eval-rst}
.. glossary::

   rotor
      Рекомендательное радио Яндекс Музыки. Представлено моделями :class:`yandex_music.rotor.station.Station`, :class:`yandex_music.rotor.dashboard.Dashboard`, :class:`yandex_music.rotor.station_result.StationResult`.

   station
      Радиостанция в рамках :term:`rotor`. Характеризуется идентификатором, настройками фильтрации, рекомендательным потоком.

   wave
      Персональная волна — поток треков, адаптирующийся к действиям пользователя. Модель :class:`yandex_music.wave.wave.Wave`.

   dashboard
      Дашборд радио — набор рекомендованных станций и метаданные для экрана радио. Модель :class:`yandex_music.rotor.dashboard.Dashboard`.

   landing
      Главный экран приложения/сайта Яндекс Музыки. Набор блоков разного типа (плейлисты, чарты, промо). Модель :class:`yandex_music.landing.landing.Landing`.

   block
      Элемент :term:`landing` — сгруппированный контент определённого типа. Модель :class:`yandex_music.landing.block.Block`.

   metatag
      Поисковый таг (жанр/настроение/эпоха) для фильтрации контента. Метатеги агрегируют альбомы, плейлисты, артистов. Модель :class:`yandex_music.metatag.metatag.Metatag`.

   chart
      Чарт — топ-список треков по стране/региону. Модель :class:`yandex_music.landing.chart.Chart`.

   promo
      Промо-блок — рекламное/акционное размещение на лендинге. Модель :class:`yandex_music.landing.promotion.Promotion`.

   supplement
      Дополнительная информация о треке: лирика, видео-клип, описание. Модель :class:`yandex_music.supplement.supplement.Supplement`.

   lyrics
      Текст песни с разметкой. Модель :class:`yandex_music.supplement.lyrics.Lyrics`, а также расширенный формат :class:`yandex_music.track.track_lyrics.TrackLyrics`.

   fade
      Параметры фейда трека (появление/затухание на границах). Модель :class:`yandex_music.track.fade.Fade`.

   radio
      См. :term:`rotor`. В разных методах API встречаются оба термина, в библиотеке каноничным считается `rotor`.

   skeleton
      UI-скелетон — структура плейсхолдеров для отрисовки экрана до загрузки данных. Модель :class:`yandex_music.skeleton.skeleton_block.SkeletonBlock`.

   shot
      Голосовая врезка ведущего между треками в :term:`wave`/:term:`rotor`. Модель :class:`yandex_music.shot.shot.Shot`.

   queue
      Очередь воспроизведения с контекстом (альбом/плейлист/радио). Модель :class:`yandex_music.queue.queue.Queue`.

   feed
      Лента событий пользователя: новые релизы любимых артистов, дейли-плейлисты, рекомендации. Модель :class:`yandex_music.feed.feed.Feed`.

   pin
      Закреплённый элемент (альбом/плейлист/артист/подкаст) в библиотеке пользователя. Модель :class:`yandex_music.pin.pin.Pin`.

   presave
      Предсохранение альбома — анонс с возможностью добавить альбом в библиотеку до его релиза. Модель :class:`yandex_music.presave.presaves.Presaves`.

   promo_code
      Промокод на подписку или скидку. Модель :class:`yandex_music.promo_code_status.PromoCodeStatus`.

   region
      Регион пользователя, определяющий доступный каталог и цены подписки. Передаётся в ряде методов API как параметр.

   like
      Лайк (добавление в избранное) трека/альбома/артиста/плейлиста/клипа. Методы миксина :class:`yandex_music._client.likes.LikesMixin`.

   dislike
      Дизлайк — сигнал «не рекомендовать этого артиста/трек». Методы миксина :class:`yandex_music._client.likes.LikesMixin`.
```
