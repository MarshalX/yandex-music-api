from math import floor
from random import random
from time import sleep

from radio import Radio

from yandex_music import Client

# API instance
client = Client(token='YOUR_TOKEN_HERE')

# Get random station
_stations = client.rotor_stations_list()
_station_random_index = floor(len(_stations) * random())
_station = _stations[_station_random_index].station
_station_id = f'{_station.id.type}:{_station.id.tag}'
_station_from = _station.id_for_from

# Radio instance
radio = Radio(client)

# start radio and get first track
first_track = radio.start_radio(_station_id, _station_from)
print('[Radio] First track is:', first_track)

# get new track every 5 sec
while True:
    sleep(5)
    next_track = radio.play_next()
    print('[Radio] Next track is:', next_track)
