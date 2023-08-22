from alive_progress import alive_bar
from typing import Iterable, Any


def progressBarIterator(
    iterable: Iterable[Any], description: str = "Progress", **kwargs
):
    with alive_bar(
        len(iterable), force_tty=True, bar="filling", spinner="waves", **kwargs
    ) as bar:
        bar.title = description
        for item in iterable:
            yield item
            bar()
