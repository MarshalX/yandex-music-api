from time import sleep

from radio import Radio

from yandex_music import Client

# API instance
client = Client(token='YOUR_API_KEY_HERE').init()

# get some track
track = client.tracks(['2816574:303266'])[0]
album = track.albums[0]
artist = track.artists[0]

# stream by track
_station_id, _station_from = f'track:{track.id}', 'track'

# stream by album
# _station_id, _station_from = f'album:{album.id}', 'album'

# stream by artist
# _station_id, _station_from = f'artist:{artist.id}', 'artist'

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
