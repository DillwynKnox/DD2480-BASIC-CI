import logging
from pathlib import Path


class LoggerService:
    def __init__(self, log_dir: str | Path = "logs", level=logging.INFO):
        """
        Initialize the LoggerService.

        :param log_dir: Directory where log files are stored
        :param level: Logging level (e.g. logging.INFO, logging.DEBUG)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.level = level

    def get_logger(self, name: str) -> logging.Logger:
        """
        get_logger returns a configured logger that writes to a file.

        :param name: Name of the logger (usually __name__)
        :return: Configured logging.Logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.level)

        # Avoid adding multiple handlers if logger already exists
        if not logger.handlers:
            log_file = self.log_dir / "ci.log"

            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger