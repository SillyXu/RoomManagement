# logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to create a logging instance."""
    # 确保 log 文件夹存在
    log_dir = os.path.join(os.getcwd(), 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 完整的日志文件路径
    log_file_path = os.path.join(log_dir, log_file)

    handler = RotatingFileHandler(log_file_path, maxBytes=20000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def get_logger(name, log_file):
    """Get a logger instance."""
    return setup_logger(name, log_file)