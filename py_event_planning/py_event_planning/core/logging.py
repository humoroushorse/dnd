"""Application root logging configurations."""

import sys

from loguru import logger

from py_event_planning.core.config import Settings


def custom_format(record: dict) -> str:
    """Custom logger format.

    Args:
        record (_type_): the object loguru has for the record

    Returns:
        _type_: custom string for formatting
    """
    loguru_default_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS zz}</green>"
        + " | <level>{level:<8}</level>"
        + " | {name}:{function}:{line}"
        + " | <cyan>{message}</cyan>"
    )
    # add context to the default formatter, see logger.bind docs:
    #    https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.bind
    extra = record.get("extra", {})
    if extra:
        loguru_default_format += " | <magenta>{extra}</magenta>"
    if extra.get("log_threads"):
        loguru_default_format += " | <red>{process}:{thread}</red>"
    return loguru_default_format + "\n"


async def init_logging(settings: Settings) -> None:
    """Create application loggers.

    Args:
        settings (Settings): application environment variables
    """
    log_level = settings.LOG_LEVEL
    log_diagnose = settings.LOG_DIAGNOSE

    logger.remove(0)
    logger.add(
        sys.stdout,
        format=custom_format,
        colorize=True,
        level=log_level,
        diagnose=log_diagnose,  # KEEP False IN PROD
        enqueue=False,
        serialize=False,
    )

    if settings.LOG_TO_FILE:
        logger.add(
            sink="logs/all/{time}.log",
            format=custom_format,
            colorize=False,
            rotation=settings.LOG_ROTATION,
            retention=settings.LOG_RETENTION,
            level=log_level,
            diagnose=log_diagnose,  # KEEP False IN PROD
            enqueue=True,
            serialize=True,
        )
        logger.add(
            sink="logs/error/{time}.log",
            format=custom_format,
            colorize=False,
            rotation=settings.LOG_ROTATION,
            retention=settings.LOG_RETENTION,
            level="ERROR",  # Only error logs
            diagnose=log_diagnose,  # KEEP False IN PROD
            enqueue=True,
            serialize=True,
        )
    logger.trace("This is a trace log!")
    logger.debug("This is a debug log!")
    logger.info("This is a info log!")
    logger.success("This is a success log!")
    logger.warning("This is a warning log!")
    logger.error("This is a error log!")
    logger.critical("This is a critical log!")
    logger.exception("This is a exception log!")
