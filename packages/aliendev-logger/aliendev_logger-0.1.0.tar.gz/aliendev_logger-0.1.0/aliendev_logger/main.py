import functools
import time
from loguru import logger

def custom_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Calling {func.__name__} with arguments {args} and kwargs {kwargs}")
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} returned {result}")
        logger.info(f"Execution time of {func.__name__}: {execution_time:.6f} seconds")
        return result
    return wrapper
