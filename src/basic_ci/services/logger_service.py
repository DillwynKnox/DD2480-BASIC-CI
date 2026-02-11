import logging
from pathlib import Path


class LoggerService:
    def __init__(self, log_dir: str | Path = "logs", level=logging.INFO):
        """
        Initialize the LoggerService with a log directory and logging level.

        Creates the log directory if it doesn't exist and sets up the base
        configuration for all loggers created by this service.

        Args:
            log_dir (Union[str, Path]): Directory where log files are stored.
                                       Defaults to "logs".
            level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
                        Defaults to logging.INFO.

        Returns:
            None
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.level = level

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a configured logger instance that writes to a file.

        This method creates or retrieves a logger with the specified name
        and configures it with a file handler that writes to 'ci.log' in the
        configured log directory. The logger uses a standardized format:
        timestamp | level | logger_name | message.

        The method prevents duplicate handlers from being added if the logger
        already exists and has been configured previously.

        Args:
            name (str): Name of the logger (typically __name__ from the calling module)

        Returns:
            logging.Logger: Configured logger instance ready for use
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