from yandex_music import Album, Artist, Client, Playlist, Track, Video

client = Client().init()

type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}


def send_search_request_and_print_result(query: str) -> None:  # noqa: C901
    search_result = client.search(query)
    if search_result is None:
        print(f'По запросу "{query}" ничего не найдено\n')
        return

    text = [f'Результаты по запросу "{query}":', '']

    best_result_text = ''
    if search_result.best is not None:
        type_ = search_result.best.type
        best = search_result.best.result

        text.append(f'❗️Лучший результат: {type_to_name.get(type_)}')

        if isinstance(best, Track):
            artists = ''
            if len(best.artists) > 0:
                artists = ' - ' + ', '.join(artist.name for artist in best.artists if artist.name is not None)
            best_result_text = f'{best.title}{artists}'
        elif isinstance(best, Artist):
            best_result_text = f'{best.name}'
        elif isinstance(best, (Album, Playlist)):
            best_result_text = f'{best.title}'
        elif isinstance(best, Video):
            best_result_text = f'{best.title} {best.text}'

        text.append(f'Содержимое лучшего результата: {best_result_text}\n')

    if search_result.artists is not None:
        text.append(f'Исполнителей: {search_result.artists.total}')
    if search_result.albums is not None:
        text.append(f'Альбомов: {search_result.albums.total}')
    if search_result.tracks is not None:
        text.append(f'Треков: {search_result.tracks.total}')
    if search_result.playlists is not None:
        text.append(f'Плейлистов: {search_result.playlists.total}')
    if search_result.videos is not None:
        text.append(f'Видео: {search_result.videos.total}')

    text.append('')
    print('\n'.join(text))


if __name__ == '__main__':
    while True:
        input_query = input('Введите поисковой запрос: ')
        send_search_request_and_print_result(input_query)
