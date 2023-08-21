from logging import Logger
from typing import Optional


def loggingHandler(logger: Optional[Logger], log_mssg):
    if logger != None:
        logger.log(logger.level, log_mssg)
    print(log_mssg)
