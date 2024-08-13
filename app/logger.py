# logger.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO):
    """Function to create a logging instance."""
    handler = RotatingFileHandler(log_file, maxBytes=20000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def get_logger(name, log_file):
    """Get a logger instance."""
    return setup_logger(name, log_file)