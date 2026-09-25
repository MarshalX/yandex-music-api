"""Удалённый пульт плеера (Ynison).

Интерактивный пример: выводит текущее состояние плеера и позволяет
управлять активным устройством (пауза/продолжить, переключение
треков, громкость) через одно постоянное соединение.
"""

import os

from yandex_music.exceptions import YnisonNoActiveDeviceError, YnisonQueueBoundaryError
from yandex_music.ynison import YnisonClient, utils

TOKEN = os.environ.get('TOKEN')
# Фиксированный идентификатор клиента в Ynison-сессии. Можно не указывать:
# по умолчанию он вычисляется из токена и тоже не меняется между запусками.
# Одновременно с одним device_id может быть подключён только один клиент.
DEVICE_ID = '9089862716d2c'


def print_state(client):
    device = client.active_device
    track = client.current_playable
    status = client.state.player_state.status
    progress = utils.get_current_progress_ms(status)

    print(f'  устройство: {device.info.title if device else "(нет активного)"}')
    print(f'  трек:       {track.title if track else "-"}')
    print(f'  пауза:      {status.paused}   прогресс: {progress}/{status.duration_ms} мс')


def set_volume(client):
    raw = input('  громкость [0.0-1.0]: ').strip()
    if raw:
        client.set_volume(float(raw))


ACTIONS = {
    '1': ('пауза', lambda c: c.pause()),
    '2': ('продолжить', lambda c: c.resume()),
    '3': ('следующий', lambda c: c.next_track()),
    '4': ('предыдущий', lambda c: c.previous_track()),
    '5': ('громкость', set_volume),
    's': ('состояние', print_state),
}


def menu():
    print()
    for key, (label, _) in ACTIONS.items():
        print(f'  {key}. {label}')
    print('  q. выход')

    return input('> ').strip().lower()


if __name__ == '__main__':
    with YnisonClient(TOKEN, device_id=DEVICE_ID).session() as client:
        print_state(client)

        while True:
            choice = menu()
            if choice == 'q':
                break

            entry = ACTIONS.get(choice)
            if entry is None:
                print(f'  неизвестное действие: {choice!r}')
                continue

            label, action = entry
            try:
                action(client)
                if choice != 's':
                    print(f'  -> {label} отправлено')
            except YnisonNoActiveDeviceError:
                print('  сейчас ничего не играет: запустите музыку на любом устройстве')
            except YnisonQueueBoundaryError:
                print('  дальше треков в очереди нет')
            except ValueError:
                print('  введите число от 0.0 до 1.0')
