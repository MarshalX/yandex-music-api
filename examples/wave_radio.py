"""Консольное радио «Моя волна».

Выбираете волну (Моя волна или занятие) и её характер, после чего треки
играют один за другим. Радио узнаёт о прослушиваниях и пропусках через
обратную связь сессии и подбирает следующие треки с их учётом.

Управление во время воспроизведения:
    Enter: следующий трек, l: нравится, d: не нравится (и дальше), q: выход.

Треки воспроизводятся установленным в системе плеером (afplay, mpv, ffplay
или cvlc). Свой плеер можно указать в переменной окружения PLAYER, например:
PLAYER="mpv --no-video". Сторонние Python-библиотеки не нужны.

Запуск: TOKEN=<ваш токен> python wave_radio.py
"""

import os
import queue
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import List, Optional, Tuple, TypeVar

from yandex_music import Client, Sequence, Track
from yandex_music.exceptions import NetworkError

T = TypeVar('T')

TOKEN = os.environ.get('TOKEN')
KNOWN_PLAYERS = [
    'afplay',
    'mpv --no-video --really-quiet',
    'ffplay -nodisp -autoexit -loglevel quiet',
    'cvlc --play-and-exit',
]


def find_player() -> List[str]:
    player = os.environ.get('PLAYER')
    if player is not None and player != '':
        return shlex.split(player)

    for command in KNOWN_PLAYERS:
        if shutil.which(command.split()[0]) is not None:
            return command.split()

    sys.exit('Не найден плеер. Установите mpv или укажите свой в переменной окружения PLAYER.')


def choose(title: str, options: List[Tuple[str, T]]) -> T:
    """Показывает нумерованный список и возвращает выбранное значение."""
    print(f'\n{title} (Enter: {options[0][0]})')
    for number, (name, _) in enumerate(options, 1):
        print(f'  {number}. {name}')

    answer = input('> ').strip()
    if answer.isdigit() and 1 <= int(answer) <= len(options):
        return options[int(answer) - 1][1]

    return options[0][1]


def choose_seeds(client: Client) -> List[str]:
    """Спрашивает, какую волну включить. Возвращает список сидов для сессии радио."""
    settings = client.rotor_wave_settings()
    if settings is None:
        sys.exit('Не удалось получить настройки волны.')

    waves = [('Моя волна', 'user:onyourwave')]
    for block in settings.blocks if settings.blocks is not None else []:
        waves.extend(
            (station.name, f'{station.id.type}:{station.id.tag}')
            for station in (block.items if block.items is not None else [])
            if station.id is not None
        )

    seeds = [choose('Какую волну включить?', waves)]

    restrictions = settings.setting_restrictions
    if restrictions is not None and restrictions.diversity is not None:
        # «Любое» (unspecified) первым, чтобы оно выбиралось по умолчанию
        values = sorted(restrictions.diversity.possible_values, key=lambda value: value.unspecified is not True)
        characters = [(value.name, value.serialized_seed) for value in values if value.serialized_seed is not None]
        seeds.append(choose('Какой характер?', characters))

    return seeds


def read_keys(keys: 'queue.Queue[str]') -> None:
    """Читает команды с клавиатуры в отдельном потоке, чтобы не мешать воспроизведению."""
    for line in sys.stdin:
        keys.put(line.strip().lower())
    keys.put('q')


def play(
    client: Client,
    session_id: str,
    batch_id: Optional[str],
    track: Track,
    player: List[str],
    keys: 'queue.Queue[str]',
) -> str:
    """Проигрывает трек и отправляет обратную связь. Возвращает команду, которой он закончился."""
    print(f'\n♪ {", ".join(track.artists_name())} - {track.title}')
    path = str(Path(tempfile.gettempdir(), 'wave_radio.mp3'))
    track.download(path, timeout=30)  # на медленной сети загрузка может надолго замирать

    _ = client.rotor_session_feedback_track_started(session_id, track.id, batch_id)
    started_at = time.time()
    process = subprocess.Popen([*player, path])

    while process.poll() is None:
        try:
            key = keys.get(timeout=0.5)
        except queue.Empty:
            continue

        if key == 'l':
            _ = client.users_likes_tracks_add(track.track_id)
            print('  ♥ добавлено в «Мне нравится»')
        elif key in ('', 'd', 'q'):
            process.terminate()
            played = time.time() - started_at
            _ = client.rotor_session_feedback_skip(session_id, track.id, played, batch_id)
            if key == 'd':
                _ = client.users_dislikes_tracks_add(track.track_id)
                print('  ✕ больше не порекомендуем')
            return key

    duration = track.duration_ms / 1000 if track.duration_ms is not None else time.time() - started_at
    _ = client.rotor_session_feedback_track_finished(session_id, track.id, duration, batch_id)
    return 'finished'


def main() -> None:
    if TOKEN is None or TOKEN == '':
        sys.exit('Укажите токен в переменной окружения TOKEN.')

    client = Client(TOKEN).init()
    player = find_player()

    seeds = choose_seeds(client)
    session = client.rotor_session_new(seeds)
    if session is None or session.radio_session_id is None:
        sys.exit('Не удалось создать сессию радио.')

    session_id, batch_id = session.radio_session_id, session.batch_id
    sequence: List[Sequence] = session.sequence if session.sequence is not None else []
    _ = client.rotor_session_feedback_radio_started(session_id, batch_id)

    print('\nEnter: следующий трек, l: нравится, d: не нравится, q: выход')
    keys: queue.Queue[str] = queue.Queue()
    threading.Thread(target=read_keys, args=(keys,), daemon=True).start()

    played_ids: List[str] = []
    while True:
        try:
            if len(sequence) == 0:
                # партия закончилась, просим следующую с уже сыгранными треками
                more = client.rotor_session_tracks(session_id, queue=played_ids)
                if more is None or more.sequence is None or len(more.sequence) == 0:
                    print('Радио не вернуло новых треков')
                    break
                sequence, batch_id = more.sequence, more.batch_id

            track = sequence.pop(0).track
            if track is None:
                continue

            played_ids.append(track.track_id)
            if play(client, session_id, batch_id, track, player, keys) == 'q':
                break
        except NetworkError as error:
            # при сбое сети переходим к следующему треку
            message = str(error)
            print(f'  ошибка сети: {message if message != "" else type(error).__name__}, пробуем дальше')
            time.sleep(1)

    print('Пока!')


if __name__ == '__main__':
    main()
