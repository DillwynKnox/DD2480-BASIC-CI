from pathlib import Path
import logging
import pytest

from basic_ci.services.logger_service import LoggerService


@pytest.fixture
def clean_logger():
    """
    clean_logger removes handlers from loggers created during tests
    to avoid side effects between test cases.
    """
    created = []

    def _register(name: str):
        logger = logging.getLogger(name)
        logger.propagate = False
        created.append(name)
        return logger

    yield _register

    # Cleanup after test
    for name in created:
        logger = logging.getLogger(name)
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            try:
                handler.close()
            except Exception:
                pass


def test_logger_creates_file_and_logs_message(tmp_path: Path, clean_logger):
    """
    test_logger_creates_file_and_logs_message verifies that LoggerService
    creates a log file and writes log entries to it.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    clean_logger("TestLogger")

    service = LoggerService(log_dir=tmp_path, level=logging.INFO)
    logger = service.get_logger("TestLogger")

    message = "CI build started"
    logger.info(message)

    # Ensure content is flushed to disk
    for handler in logger.handlers:
        handler.flush()

    log_file = tmp_path / "ci.log"
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert message in content
    assert "INFO" in content
    assert "TestLogger" in content


def test_logger_prevents_duplicate_handlers(tmp_path: Path, clean_logger):
    """
    test_logger_prevents_duplicate_handlers verifies that calling get_logger
    multiple times does not attach multiple handlers to the same logger.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    clean_logger("UniqueLogger")

    service = LoggerService(log_dir=tmp_path, level=logging.INFO)

    logger1 = service.get_logger("UniqueLogger")
    logger2 = service.get_logger("UniqueLogger")

    assert logger1 is logger2
    assert len(logger1.handlers) == 1

    logger1.info("one message")

    for handler in logger1.handlers:
        handler.flush()

    content = (tmp_path / "ci.log").read_text(encoding="utf-8")
    assert content.count("one message") == 1