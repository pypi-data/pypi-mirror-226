from alive_progress import alive_bar
import pandas as pd
from typing import Callable, Optional, TypeVar, Any, Dict


ArgsType = TypeVar("ArgsType", bound=Dict)


async def processCSVInChunks(
    csv_file: str,
    process_function: Callable[[pd.DataFrame, Any], pd.DataFrame],
    pf_args: ArgsType,
    chunk_size: Optional[int] = 10000,
):
    """
    Process any CSV file in chunks instead of whole file at once\n\n
    `csv_file`: Path to the csv file.\n
    `chunk_size`: Size of chunks to work with\n
    :strong:`process_function`: The function containing the main processing you want to get done.\n
    `pf_args`: Arguments for the function in a dict eg:-\n
                def deleteRowsInCSV(dataframe,delete_rows):\n
                    # ...delete rows from csv.\n
                await processCSVInChunks(path_to_csv,deleteRowsInCSV,{delete_rows:20})\n

    """
    # Create a generator to read the CSV file in chunks
    chunk_reader = pd.read_csv(csv_file, chunksize=chunk_size)

    # Process each chunk and concatenate the results
    processed_chunks = []
    total_chunks = int(sum(1 for row in open(csv_file, "r")) / chunk_size)
    with alive_bar(total_chunks, force_tty=True, bar="filling", spinner="waves") as bar:
        bar.title = "Processing file -> " + csv_file
        for chunk in chunk_reader:
            processed_chunk = process_function(chunk, pf_args)
            processed_chunks.append(processed_chunk)
            bar()
    # Concatenate the processed chunks into a single DataFrame
    df = pd.concat(processed_chunks, ignore_index=True)

    return df
