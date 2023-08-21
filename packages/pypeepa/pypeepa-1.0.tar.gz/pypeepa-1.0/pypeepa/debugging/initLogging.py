import logging


def initLogging(app_name, level):
    level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
        "FATAL": logging.CRITICAL,
    }

    if level not in level_mapping:
        raise ValueError("Invalid log level specified")

    level_in_int = level_mapping[level]

    # Initialize logging
    logging.basicConfig(
        filename=f"ExceptionLogs-{app_name}.log",
        format="%(asctime)s %(message)s",
    )

    logger = logging.getLogger()
    logger.setLevel(level_in_int)
    logger.debug(f"------------------{app_name} initialised!------------------")

    return logger
