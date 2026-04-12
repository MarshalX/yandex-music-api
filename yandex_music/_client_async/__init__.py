import functools
import logging
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


def log(method: F) -> F:
    """Декоратор для логирования вызовов методов клиента."""
    logger = logging.getLogger(method.__module__)

    @functools.wraps(method)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401:
        logger.debug(f'Entering: {method.__name__}')

        result = await method(*args, **kwargs)
        logger.debug(result)

        logger.debug(f'Exiting: {method.__name__}')

        return result

    return wrapper
