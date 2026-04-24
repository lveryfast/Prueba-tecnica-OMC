import logging
import sys
from typing import Any

from pythonjsonlogger import json

from app.config import settings


class StructuredFormatter(json.JsonFormatter):
    """JSON formatter with custom fields for structured logging."""

    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["module"] = record.module
        log_record["function"] = record.funcName
        log_record["line"] = record.lineno


def setup_logging() -> None:
    """Configure structured logging for production."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    if settings.ENVIRONMENT == "production":
        formatter = StructuredFormatter(
            "%(asctime)s %(level)s %(name)s %(message)s",
            rename_fields={"asctime": "timestamp", "name": "service"}
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)


class LogContext:
    """Context manager for adding extra fields to log messages."""

    def __init__(self, **extra: Any) -> None:
        self.extra = extra
        self.old_factory = logging.getLogRecordFactory()

    def __enter__(self) -> "LogContext":
        def record_factory(*args: Any, **kwargs: Any) -> logging.LogRecord:
            record = self.old_factory(*args, **kwargs)
            for key, value in self.extra.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self

    def __exit__(self, *args: Any) -> None:
        logging.setLogRecordFactory(self.old_factory)