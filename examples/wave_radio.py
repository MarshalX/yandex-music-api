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

from yandex_music import Client
from yandex_music.exceptions import NetworkError

TOKEN = os.environ.get('TOKEN')
KNOWN_PLAYERS = [
    'afplay',
    'mpv --no-video --really-quiet',
    'ffplay -nodisp -autoexit -loglevel quiet',
    'cvlc --play-and-exit',
]


def find_player():
    if os.environ.get('PLAYER'):
        return shlex.split(os.environ['PLAYER'])

    for command in KNOWN_PLAYERS:
        if shutil.which(command.split()[0]):
            return command.split()

    sys.exit('Не найден плеер. Установите mpv или укажите свой в переменной окружения PLAYER.')


def choose(title, options):
    """Показывает нумерованный список и возвращает выбранное значение."""
    print(f'\n{title} (Enter: {options[0][0]})')
    for number, (name, _) in enumerate(options, 1):
        print(f'  {number}. {name}')

    answer = input('> ').strip()
    if answer.isdigit() and 1 <= int(answer) <= len(options):
        return options[int(answer) - 1][1]

    return options[0][1]


def choose_seeds(client):
    """Спрашивает, какую волну включить. Возвращает список сидов для сессии радио."""
    settings = client.rotor_wave_settings()

    waves = [('Моя волна', 'user:onyourwave')]
    for block in settings.blocks:
        for station in block.items:
            waves.append((station.name, f'{station.id.type}:{station.id.tag}'))

    # «Любое» (unspecified) первым, чтобы оно выбиралось по умолчанию
    values = sorted(settings.setting_restrictions.diversity.possible_values, key=lambda value: not value.unspecified)
    characters = [(value.name, value.serialized_seed) for value in values]

    return [choose('Какую волну включить?', waves), choose('Какой характер?', characters)]


def read_keys(keys):
    """Читает команды с клавиатуры в отдельном потоке, чтобы не мешать воспроизведению."""
    for line in sys.stdin:
        keys.put(line.strip().lower())
    keys.put('q')


def play(client, session, track, player, keys):
    """Проигрывает трек и отправляет обратную связь. Возвращает команду, которой он закончился."""
    session_id, batch_id = session.radio_session_id, session.batch_id

    print(f'\n♪ {", ".join(track.artists_name())} - {track.title}')
    path = os.path.join(tempfile.gettempdir(), 'wave_radio.mp3')
    track.download(path, timeout=30)  # на медленной сети загрузка может надолго замирать

    client.rotor_session_feedback_track_started(session_id, track.id, batch_id)
    started_at = time.time()
    process = subprocess.Popen([*player, path])

    while process.poll() is None:
        try:
            key = keys.get(timeout=0.5)
        except queue.Empty:
            continue

        if key == 'l':
            client.users_likes_tracks_add(track.track_id)
            print('  ♥ добавлено в «Мне нравится»')
        elif key in ('', 'd', 'q'):
            process.terminate()
            played = time.time() - started_at
            client.rotor_session_feedback_skip(session_id, track.id, played, batch_id)
            if key == 'd':
                client.users_dislikes_tracks_add(track.track_id)
                print('  ✕ больше не порекомендуем')
            return key

    client.rotor_session_feedback_track_finished(session_id, track.id, track.duration_ms / 1000, batch_id)
    return 'finished'


def main():
    if not TOKEN:
        sys.exit('Укажите токен в переменной окружения TOKEN.')

    client = Client(TOKEN).init()
    player = find_player()

    seeds = choose_seeds(client)
    session = client.rotor_session_new(seeds)
    client.rotor_session_feedback_radio_started(session.radio_session_id, session.batch_id)

    print('\nEnter: следующий трек, l: нравится, d: не нравится, q: выход')
    keys = queue.Queue()
    threading.Thread(target=read_keys, args=(keys,), daemon=True).start()

    played_ids = []
    while True:
        try:
            if not session.sequence:
                # партия закончилась, просим следующую с уже сыгранными треками
                more = client.rotor_session_tracks(session.radio_session_id, queue=played_ids)
                session.sequence, session.batch_id = more.sequence, more.batch_id

            track = session.sequence.pop(0).track
            played_ids.append(track.track_id)
            if play(client, session, track, player, keys) == 'q':
                break
        except NetworkError as error:
            # при сбое сети переходим к следующему треку
            print(f'  ошибка сети: {error or type(error).__name__}, пробуем дальше')
            time.sleep(1)

    print('Пока!')


if __name__ == '__main__':
    main()
