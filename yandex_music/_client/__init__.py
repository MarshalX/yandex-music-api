#################################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/__init__.py. DON'T EDIT IT BY HANDS #
#################################################################################################

import functools
import logging
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


def log(method: F) -> F:
    """Декоратор для логирования вызовов методов клиента."""
    logger = logging.getLogger(method.__module__)

    @functools.wraps(method)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401:
        logger.debug(f'Entering: {method.__name__}')

        result = method(*args, **kwargs)
        logger.debug(result)

        logger.debug(f'Exiting: {method.__name__}')

        return result

    return wrapper
