from typing import Union


def convert_track_id_to_number(track_id: Union[str, int]) -> int:
    """TODO"""
    if isinstance(track_id, str):
        track_id = int(track_id.split(':')[0])

    return track_id
