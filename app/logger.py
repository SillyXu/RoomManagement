# logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import threading

class ThreadSafeLogger:
    def __init__(self, name, log_file, level=logging.INFO):
        self.name = name
        self.log_file = log_file
        self.level = level
        self.lock = threading.Lock()
        self.logger = self.setup_logger()

    def setup_logger(self):
        """Function to create a logging instance."""
        # 确保 log 文件夹存在
        log_dir = os.path.join(os.getcwd(), 'log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 完整的日志文件路径
        log_file_path = os.path.join(log_dir, self.log_file)

        # 设置 TimedRotatingFileHandler，每年滚动一次
        handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=365, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.addHandler(handler)

        return logger

    def info(self, message):
        with self.lock:
            try:
                self.logger.info(message)
            except PermissionError as e:
                print(f"PermissionError: {e}")
            except Exception as e:
                print(f"Error writing to log file: {e}")

    def warning(self, message):
        with self.lock:
            try:
                self.logger.warning(message)
            except PermissionError as e:
                print(f"PermissionError: {e}")
            except Exception as e:
                print(f"Error writing to log file: {e}")

    def error(self, message):
        with self.lock:
            try:
                self.logger.error(message)
            except PermissionError as e:
                print(f"PermissionError: {e}")
            except Exception as e:
                print(f"Error writing to log file: {e}")

    def debug(self, message):
        with self.lock:
            try:
                self.logger.debug(message)
            except PermissionError as e:
                print(f"PermissionError: {e}")
            except Exception as e:
                print(f"Error writing to log file: {e}")

def get_logger(name, log_file):
    """Get a thread-safe logger instance."""
    return ThreadSafeLogger(name, log_file)