import concurrent.futures
import time
import psutil
from typing import Optional, Callable, Any, Iterable
import logging


def loggingHandler(logger, log_mssg):
    if logger != None:
        logger.debug(log_mssg)
    print(log_mssg)


def concurrentFutures(
    process_function: Callable[[Any], Any],
    divided_tasks: Iterable[Any],
    max_workers: Optional[int] = 4,
    logger: Optional[logging.Logger] = None,
):
    """
    Wrapper function to run multiple instances of the same function parallely,

    `process_function`: The function that contains your processing logic.

    `divided_tasks`:  The parameters for the process_function, It contains the divided tasks parameters in an Iterable.

    `max_workers`: (Optional) The maximum number parallel processes.

    `logger`: (Optional) You can pass a logging object if you already initialised one.
    """
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for task, time_taken in zip(
            divided_tasks, executor.map(process_function, divided_tasks)
        ):
            try:
                loggingHandler(
                    logger=logger,
                    log_mssg="Start: {} Time taken: {}".format(task, time_taken),
                )
            except Exception as e:
                loggingHandler(
                    logger=logger,
                    log_mssg="Error occurred on task: {} --> Error Report: {}".format(
                        task, e
                    ),
                )

    loggingHandler(
        logger=logger, log_mssg="Total time taken: {}".format(time.time() - start)
    )

    # Print memory usage
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)  # in megabytes
    print("Memory usage:", memory_usage, "MB")
