from loguru import logger
from pathlib import Path

class LogManager:
    def __init__(self, log_file):
        # Ensure the directory exists, and create it if not
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_path = log_dir / log_file
        # Create a file handler
        self.log_handler = logger.add(log_path, rotation="10 MB", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}")
        
    def log(self, level, message):
        if level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
        elif level == "success":
            logger.success(message)

    def close_log(self):
        logger.remove(self.log_handler)
