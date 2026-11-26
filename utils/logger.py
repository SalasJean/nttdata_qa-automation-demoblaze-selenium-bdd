"""Configuracion centralizada del logger del proyecto."""

import logging
import sys

from config.settings import LOG_LEVEL

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "automation") -> logging.Logger:
    """Devuelve un logger configurado con formato legible y sin handlers duplicados."""
    logger = logging.getLogger(name)
    level = getattr(logging, LOG_LEVEL, logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(fmt=_LOG_FORMAT, datefmt=_DATE_FORMAT))
        logger.addHandler(handler)

    logger.propagate = False
    return logger
