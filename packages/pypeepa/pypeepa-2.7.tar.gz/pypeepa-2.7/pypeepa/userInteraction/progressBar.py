from alive_progress import alive_bar
from typing import Iterable, Any, Callable, Optional
from pypeepa.checks.checkIfListIsAllNone import checkIfListIsAllNone


def progressBar(
    func: Callable[[Any], Any],
    iterable: Iterable[Any],
    iterable_length: Optional[int] = None,
    desc: Optional[str] = "Progress",
):
    """
    Shows a progress bar for any iterable using alive_progress's (https://pypi.org/project/alive-progress/) alive_bar.\n
    @param: `func`: The function for the iterable.\n
    @param: `iterable`: The iterable object that you want the progressbar to show for.\n
    @param: `iterable_length`: (Optional) The length of the iterable if the length of iterable cannot be found using len(iterable), for instance a TextFileReader type iterable.\n
    @param: `desc`: (Optional) Any text to display in front of the progress bar.\n
    @return:
        If the func has return values than return the values in a list else return None\n
    """
    if iterable_length == None:
        iterable_length = len(iterable)

    def wrapper(*args, **kwargs):
        results = []

        with alive_bar(
            iterable_length,
            force_tty=True,
            bar="filling",
            spinner="waves",
        ) as bar:
            bar.title = desc
            for item in iterable:
                result = func(item, *args, **kwargs)
                results.append(result)
                bar()

        if checkIfListIsAllNone(results):
            return None

        return results

    return wrapper
