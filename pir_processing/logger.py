""" Logging."""

import logging


def set_logging():
    """Create a logger.

    Args:
        name (str): the file name (you should always pass the __name__ variable).

    Returns:
        logging.Logger: the logger.
    """
    log_format = "%(asctime)s - %(levelname)s - %(name)s: %(message)s"
    formatter = logging.Formatter(log_format)
    
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(formatter)
    handler_stream.setLevel(level=logging.INFO)
    logging.basicConfig(level=logging.INFO, format=log_format, handlers=[handler_stream],)
