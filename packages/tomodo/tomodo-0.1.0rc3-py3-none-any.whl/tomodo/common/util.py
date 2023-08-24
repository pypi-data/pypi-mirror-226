import functools
import logging
import time
from typing import Tuple, Type

logger = logging.getLogger("rich")


def parse_semver(version_str: str) -> (str, str, str):
    try:
        [maj_v, min_v, patch] = version_str.split(".")
        return int(maj_v), int(min_v), patch
    except ValueError:
        pass
    try:
        [maj_v, min_v] = version_str.split(".")
        return int(maj_v), int(min_v), None
    except ValueError:
        raise


def with_retry(max_attempts: int = 5, delay: int = 1, retryable_exc: Tuple[Type[Exception], ...] = (Exception,)):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except retryable_exc as e:
                    logger.exception("%s: Attempt %d failed", func.__name__, attempts + 1)
                    attempts += 1
                    time.sleep(delay)
            logger.error("%s failed after %d attempts", func.__name__, max_attempts)
            raise Exception(f"{func.__name__} failed after {max_attempts} attempts")

        return wrapper_retry

    return decorator_retry
