import logging
import os
from typing import Optional

import colorlog
from google.cloud import logging as cloud_logging

# NOTE: it is recommended to use setup_logging instead.
LOGGING_FORMAT = "%(asctime)s %(levelname)-7s %(message)s  [%(name)s]"


_ENV = os.getenv("ENV", "development").lower()
_IS_PRODUDCTION = _ENV != "development" or os.getenv("K_REVISION")


logger = logging.getLogger(__name__)


def setup_google_cloud_logging(level: int = logging.INFO) -> None:
    """
    Configure Google Cloud Logging client (when in a production environment).

    This basically means that python logging levels are correctly parsed by
    Google Cloud + structured logs are supported. Note that we require
    google-cloud-logging@3.x:
    - https://github.com/googleapis/python-logging/pull/316
    - https://github.com/googleapis/python-logging/pull/339

    Example:
        logging.info("Normal text based log message")
        logging.info({"message": "Structured JSON log", "obj": {}})  # message is shown specially in Cloud logging
        logging.info({"a": 1, "b": 2})
    """
    if not _IS_PRODUDCTION:
        logging.info(
            "Skipping Google Cloud logging (local environment detected from environement variables ENV/K_REVISION)"
        )
        return

    client = cloud_logging.Client()  # type: ignore
    client.get_default_handler()  # type: ignore
    client.setup_logging(log_level=level)  # type: ignore


def setup_development_logging(level: int = logging.INFO) -> None:
    """
    Configure local development logging. Recommended way is using the setup_logging.
    """
    root_logger = logging.getLogger("")
    if not root_logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(asctime)s %(log_color)s%(levelname)-7s %(message)s  [%(name)s]"
            )
        )
        color_logger = colorlog.getLogger()
        color_logger.addHandler(handler)
        color_logger.setLevel(level)

    class StructuredLogHelper(logging.StreamHandler):
        """
        Helper to make structured logs transition easier
        """

        def emit(self, record):
            msg = record.msg
            if isinstance(msg, dict) and "message" not in msg:
                logger.warning(
                    f"Structured logs warning: Please add 'message' key to log '{msg}'"
                )
                return

            if not isinstance(msg, (str, dict)):
                logger.warning(
                    f"Structured logs warning: Unexpected log type {type(msg)}, expected str or dict"
                )

    logging.getLogger().addHandler(StructuredLogHelper())


def setup_logging(
    log_level_development: int = logging.DEBUG,
    log_level_production: int = logging.INFO,
) -> None:
    """
    Enable the recommended logging setup for development and production.
    """

    if not _IS_PRODUDCTION:
        setup_development_logging(log_level_development)
    else:
        setup_google_cloud_logging(log_level_production)
