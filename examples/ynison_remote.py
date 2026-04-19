"""Удалённый пульт плеера (Ynison).

Интерактивный пример: выводит текущее состояние плеера и позволяет
управлять активным устройством (пауза/продолжить, переключение
треков, громкость).
"""

import os

from yandex_music.ynison import simple

TOKEN = os.environ.get('TOKEN')
# Фиксированный идентификатор клиента избавляет от накопления призрачных
# устройств в Ynison-сессии: иначе каждый запуск регистрирует новое.
DEVICE_ID = '9089862716d2c'


def print_state(token):
    state = simple.get_state(token, device_id=DEVICE_ID)

    queue = state.player_state.player_queue
    status = state.player_state.status
    idx = queue.current_playable_index
    total = len(queue.playable_list)
    title = queue.playable_list[idx].title if 0 <= idx < total else '-'

    print(f'  активное устройство: {state.active_device_id_optional or "(нет)"}')
    print(f'  трек:     [{idx + 1}/{total}] {title}')
    print(f'  пауза:    {status.paused}   прогресс: {status.progress_ms}/{status.duration_ms} мс')


def set_volume(token):
    raw = input('  громкость [0.0-1.0]: ').strip()
    if not raw:
        return

    simple.set_volume(token, float(raw), device_id=DEVICE_ID)


ACTIONS = {
    '1': ('пауза', lambda t: simple.pause(t, device_id=DEVICE_ID)),
    '2': ('продолжить', lambda t: simple.resume(t, device_id=DEVICE_ID)),
    '3': ('следующий', lambda t: simple.next_track(t, device_id=DEVICE_ID)),
    '4': ('предыдущий', lambda t: simple.previous_track(t, device_id=DEVICE_ID)),
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
    print_state(TOKEN)

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
            action(TOKEN)
            if choice != 's':
                print(f'  -> {label} отправлено')
        except Exception as e:
            print(f'  ошибка: {e}')
