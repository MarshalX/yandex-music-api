from typing import Union


def convert_track_id_to_number(track_id: Union[str, int]) -> int:
    """Переобразование идентификатора трека в номерной формат.

    Note:
        Преобразует ID в формате "{track_id}:{album}" в track_id.

        Преобразует ID в формате "{track_id}" в track_id.

    Args:
        track_id (:obj:`str` | :obj:`int`): Уникальный идентификатора трека.

    Returns:
        :obj:`int`: Уникальный идентификатора трека в номерном формате.
    """
    if isinstance(track_id, str):
        track_id = int(track_id.split(':')[0])

    return track_id
