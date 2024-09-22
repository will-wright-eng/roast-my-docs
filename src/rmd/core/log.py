import sys
import logging

from rmd.core.config import file_paths


def get_logger(name, debug=True, log_to_file=True):
    """
    Configure and get a logger with the given name.
    """
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Stream handler (console output)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(log_level)

    # File handler
    if log_to_file:
        file_handler = logging.FileHandler(file_paths.log_file)
        file_handler.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    stream_handler.setFormatter(formatter)
    if log_to_file:
        file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(stream_handler)
        if log_to_file:
            logger.addHandler(file_handler)

    return logger


logger = get_logger(__name__, debug=False)
