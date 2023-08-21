import json
from typing import Optional, List, Any, Callable
from logging import Logger


async def asyncReadJSON(
    file_name: str, loggingHandler=Optional[Callable[[Logger, str], None]]
) -> List[Any]:
    """
    Reads a .json file and returns the result.\n
    @param: `file_name`: Name of the .json file\n
    @param: `loggingHandler`: (Optional)loggingHandler function from pypeepa.utils\n
    @return: Returns the json data in an array or empty array if any error occurs.\n
    """

    read_data = []

    try:
        with open(file_name, "r") as openfile:
            read_data = json.load(openfile)
    except FileNotFoundError:
        fnf_mssg = f"File '{file_name}' not found."
        print(fnf_mssg) if not loggingHandler else loggingHandler(log_mssg=fnf_mssg)
    except json.JSONDecodeError as e:
        jde_mssg = f"Error decoding JSON in '{file_name}': {e}"
        print(jde_mssg) if not loggingHandler else loggingHandler(log_mssg=jde_mssg)
    except Exception as e:
        exc_mssg = f"An error occurred while reading '{file_name}': {e}"
        print(exc_mssg) if not loggingHandler else loggingHandler(log_mssg=exc_mssg)

    return read_data
