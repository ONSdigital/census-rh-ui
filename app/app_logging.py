import logging
import os
import sys


from structlog import configure
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import add_log_level, LoggerFactory, ProcessorFormatter


def logger_initial_config(service_name=None, log_level=None,):

    if not log_level:
        log_level = os.getenv("LOG_LEVEL", "INFO")
    if not service_name:
        service_name = "respondent-home"

    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
    }

    logger_date_format = "%Y-%m-%dT%H:%M:%s"

    def add_service(_1, _2, event_dict):
        """
        Add the service name to the event dict.
        """
        event_dict["service"] = service_name
        return event_dict

    shared_processors = [
            add_log_level,
            TimeStamper(fmt=logger_date_format, utc=True, key="created"),
            add_service,
    ]

    configure(
        processors=shared_processors + [
            ProcessorFormatter.wrap_for_formatter
        ],
        logger_factory=LoggerFactory(),
    )

    formatter = ProcessorFormatter(
        processor=JSONRenderer(),
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(levels[log_level])
