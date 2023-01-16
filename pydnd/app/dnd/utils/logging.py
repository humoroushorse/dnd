"""Logging utils."""
import functools
from typing import Callable

from loguru import logger


def debug_input(func: Callable) -> Callable:
    """Python decorator for logging function input arguments.

    Args:
        func (_type_): _description_

    Returns:
        _type_: function wrapper
    """

    @functools.wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Callable:
        result = func(*args, **kwargs)
        # logger.debug(f"{func.__name__} called with arguments: {args}")
        logger.debug(f"{func.__name__} called with keyword arguments: {kwargs}")
        # logger.debug(f"{func.__name__} returned {result}")
        return result

    return wrapper
