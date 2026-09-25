# 📻 Радио

Радио (внутреннее название — rotor) — бесконечный поток треков, который подбирается под пользователя и уточняется по ходу прослушивания. Сюда относятся «Моя волна», волны по занятиям и настроению, потоки по жанру, исполнителю, альбому или треку, а также генеративные станции с музыкой от нейросети.

## Сиды и волны

Любая волна описывается набором **сидов** — строк вида `тип:тег`:

| Сид | Что играет |
|-----|------------|
| `user:onyourwave` | Моя волна |
| `activity:wake-up`, `mood:sad` | Волна по занятию или настроению |
| `genre:rock` | Поток по жанру |
| `artist:12345`, `album:12345`, `track:12345` | Поток по исполнителю, альбому или треку |
| `settingDiversity:discover`, `settingLanguage:russian` | Настройки волны: характер, язык, настроение |

Сиды можно комбинировать: `['user:onyourwave', 'settingDiversity:discover']` — «Моя волна» только с незнакомыми треками.

Доступные занятия и значения настроек возвращает {meth}`rotor_wave_settings <yandex_music._client.wave.WaveMixin.rotor_wave_settings>`. У каждого значения настройки есть готовый сид в поле {attr}`serialized_seed <yandex_music.rotor.value.Value.serialized_seed>`:

``` python
settings = client.rotor_wave_settings()

for block in settings.blocks:
    for station in block.items:
        print(station.name, f'{station.id.type}:{station.id.tag}')  # Просыпаюсь activity:wake-up

for value in settings.setting_restrictions.diversity.possible_values:
    print(value.name, value.serialized_seed)  # Незнакомое settingDiversity:discover
```

## Сессии радио

Сессия — актуальный способ слушать радио, им пользуются приложения Яндекс Музыки. Сессия создаётся по сидам, выдаёт треки партиями и принимает обратную связь о прослушивании, по которой подбирает следующие треки.

``` python
session = client.rotor_session_new(['user:onyourwave'])
client.rotor_session_feedback_radio_started(session.radio_session_id, session.batch_id)

played = []
for item in session.sequence:
    track = item.track
    played.append(track.track_id)

    client.rotor_session_feedback_track_started(session.radio_session_id, track.id, session.batch_id)
    # ... воспроизведение трека ...
    client.rotor_session_feedback_track_finished(
        session.radio_session_id, track.id, track.duration_ms / 1000, session.batch_id
    )

# Следующая партия: передайте уже сыгранные треки, чтобы они не повторились
more = client.rotor_session_tracks(session.radio_session_id, queue=played)
```

Полный интерактивный пример с воспроизведением — [консольное радио «Моя волна»](examples.wave_radio.md).

### Обратная связь

Для частых событий есть отдельные методы: `rotor_session_feedback_radio_started`, `..._track_started`, `..._track_finished` и `..._skip`. Остальные события отправляются через {meth}`rotor_session_feedback <yandex_music._client.rotor_sessions.RotorSessionsMixin.rotor_session_feedback>` с моделью {class}`yandex_music.SessionEvent`:

``` python
from yandex_music import SessionEvent, SessionPlayable

event = SessionEvent('like', '2024-01-01T12:00:00.000Z', track_id='12345')
client.rotor_session_feedback(session.radio_session_id, event, session.batch_id)

# События playableItem* описывают проигрываемый объект: трек или клип
event = SessionEvent(
    'playableItemStarted', '2024-01-01T12:00:00.000Z', playable=SessionPlayable('clip', id='12345')
)
client.rotor_session_feedback(session.radio_session_id, event)
```

Обязательные поля зависят от типа события:

| События | Обязательные поля, кроме `timestamp` |
|---------|--------------------------------------|
| `radioStarted`, `combinedQueueStarted`, `ad` | — |
| `trackStarted`, `like`, `unlike`, `undislike` | `track_id` |
| `trackFinished`, `skip`, `dislike` | `track_id`, `total_played_seconds` |
| `playableItemStarted`, `playableItemLike`, `playableItemUnlike`, `playableItemUndislike` | `playable` |
| `playableItemFinished`, `playableItemSkip`, `playableItemDislike` | `playable`, `total_played_seconds` |

:::{note}
События `like` и `dislike` влияют только на рекомендации в текущей сессии и **не меняют** коллекцию пользователя. Чтобы трек попал в «Мне нравится», используйте {meth}`users_likes_tracks_add <yandex_music._client.likes.LikesMixin.users_likes_tracks_add>`.

Время события передавайте строкой в формате ISO 8601 (`2024-01-01T12:00:00.000Z`). Методы-сокращения подставляют текущее время сами.
:::

Несколько событий можно отправить одним запросом: {meth}`rotor_session_feedbacks <yandex_music._client.rotor_sessions.RotorSessionsMixin.rotor_session_feedbacks>` для одной сессии и {meth}`rotor_sessions_feedbacks <yandex_music._client.rotor_sessions.RotorSessionsMixin.rotor_sessions_feedbacks>` сразу для нескольких. Обратную связь можно передать и вместе с запросом следующей партии: параметр `feedbacks` у {meth}`rotor_session_tracks <yandex_music._client.rotor_sessions.RotorSessionsMixin.rotor_session_tracks>`.

### Последняя волна

{meth}`rotor_wave_last <yandex_music._client.wave.WaveMixin.rotor_wave_last>` возвращает волну, которую пользователь запускал последней (она обновляется при создании сессии), а {meth}`rotor_wave_last_reset <yandex_music._client.wave.WaveMixin.rotor_wave_last_reset>` сбрасывает её на «Мою волну».

## Комбинированные сессии

Комбинированная сессия смешивает треки и клипы (например, подборка «Время клипов»). Витрину возвращает {meth}`rotor_combined_session_landing <yandex_music._client.rotor_sessions.RotorSessionsMixin.rotor_combined_session_landing>`, сессию создаёт {meth}`rotor_combined_session_new <yandex_music._client.rotor_sessions.RotorSessionsMixin.rotor_combined_session_new>`:

``` python
landing = client.rotor_combined_session_landing(['CLIP', 'TRACK'])
for item in landing.list:
    print(item.type, item.data.title)  # CLIP Pieces
```

## Генеративные станции

Генеративные станции (`generative:focus`, `generative:energy`, `generative:calm`, `generative:relax`) играют бесконечный поток музыки, созданной нейросетью. Вместо треков у них один аудиопоток:

``` python
stream = client.rotor_station_stream('generative:focus')
print(stream.data.title, stream.stream.url)  # Вдохновение https://...

state = client.rotor_station_stream_feedback('generative:focus', 'streamPlay', stream.stream.id)
print(state.not_paused)  # True
```

Известные типы обратной связи генеративных станций: `streamStarted`, `streamPlay`, `streamPause`.

## Станции (устаревший интерфейс)

До появления сессий радио работало через станции: {meth}`rotor_station_tracks <yandex_music._client.radio.RadioMixin.rotor_station_tracks>` выдаёт партию треков, а {meth}`rotor_station_feedback <yandex_music._client.radio.RadioMixin.rotor_station_feedback>` принимает обратную связь. Этот интерфейс по-прежнему работает, но для нового кода лучше использовать сессии: ответ станции уже содержит идентификатор сессии ({attr}`radio_session_id <yandex_music.rotor.station_tracks_result.StationTracksResult.radio_session_id>`), а новые возможности (события `playableItem*`, комбинированные сессии) доступны только в сессиях.

Интерфейс станций остаётся полезным для получения информации о станциях: {meth}`rotor_stations_list <yandex_music._client.radio.RadioMixin.rotor_stations_list>`, {meth}`rotor_stations_dashboard <yandex_music._client.radio.RadioMixin.rotor_stations_dashboard>`, {meth}`rotor_station_info <yandex_music._client.radio.RadioMixin.rotor_station_info>` и сохранённых настроек волны {meth}`rotor_station_settings2 <yandex_music._client.radio.RadioMixin.rotor_station_settings2>`.

## Справочник

```{eval-rst}
.. grid:: 2
   :gutter: 2

   .. grid-item-card:: :octicon:`broadcast;1em;sd-mr-1` Сессии радио
      :link: yandex_music._client.rotor_sessions
      :link-type: doc

      ``rotor_session_new``, ``rotor_session_tracks``, ``rotor_session_clone``, ``rotor_session_feedback``, ``rotor_session_feedbacks``, ``rotor_sessions_feedbacks``, ``rotor_combined_session_new``, ``rotor_combined_session_next``, ``rotor_combined_session_landing``

   .. grid-item-card:: :octicon:`pulse;1em;sd-mr-1` Волна
      :link: yandex_music._client.wave
      :link-type: doc

      ``rotor_wave_last``, ``rotor_wave_last_reset``, ``rotor_wave_settings``

   .. grid-item-card:: :octicon:`rss;1em;sd-mr-1` Станции
      :link: yandex_music._client.radio
      :link-type: doc

      ``rotor_stations_list``, ``rotor_stations_dashboard``, ``rotor_station_info``, ``rotor_station_tracks``, ``rotor_station_feedback``, ``rotor_station_settings2``, ``rotor_station_stream``, ``rotor_station_stream_feedback``, ``rotor_account_status``

   .. grid-item-card:: :octicon:`file-binary;1em;sd-mr-1` Модели
      :link: yandex_music.rotor
      :link-type: doc

      ``RotorSession``, ``RotorSessionTracks``, ``SessionEvent``, ``SessionFeedback``, ``CombinedSession``, ``GenerativeStream``, ``Station``, ``Sequence`` и другие
```
