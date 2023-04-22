# Пример работы с радио

Документация:
- [rotor_station_tracks](https://yandex-music.readthedocs.io/en/latest/yandex_music.client.html#yandex_music.client.Client.rotor_station_tracks) – 
  Получение цепочки треков определённой станции. Читайте примечание.
  
Примеры:
- [radio.py](radio.py) – класс-обёртка над методами клиента Яндекс.Музыка. 
  Отправка фидбека о начале и завершении трека, обновление пачек треков.
- [radio_example.py](radio_example.py) – пример использования класса-обёртки 
  для радио.
- [stream_example.py](stream_example.py) – пример использования класса-обёртки
  для запуска потока (похожих) по треку, альбому и исполнителю.

