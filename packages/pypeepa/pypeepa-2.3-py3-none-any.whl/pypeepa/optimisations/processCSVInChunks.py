from alive_progress import alive_bar
import pandas as pd
from typing import Callable, Optional, TypeVar, Any, Dict


ArgsType = TypeVar("ArgsType", bound=Dict)


def processCSVInChunks(
    csv_file: str,
    process_function: Callable[[pd.DataFrame, Any], pd.DataFrame],
    pf_args: ArgsType,
    chunk_size: Optional[int] = 10000,
    hide_progress_bar: Optional[bool] = False,
):
    """
    Process any CSV file in chunks instead of whole file at once\n\n
    @param: `csv_file`: Path to the csv file.\n
    @param:`process_function`: The function containing the main processing you want to get done.\n
    @param:`pf_args`: Arguments for the function in a dict eg:-\n
                def deleteRowsInCSV(df,`pf_args`):\n
                    # ...delete rows from csv.\n
                    df=df.drop(`pf_args["delete_rows"]`)\n
                    return df\n
                processCSVInChunks("test.csv", deleteRowsInCSV, `{"delete_rows":range(1,20)}`)\n
    @param:`chunk_size`: (Optional) Size of chunks to work with\n
    @param:`hide_progress_bar`: (Optional) Set to True if you dont want the progress bar that comes with this\n
    @return: Dataframe containing the processed results.
    """

    # Create a generator to read the CSV file in chunks
    chunk_reader = pd.read_csv(csv_file, chunksize=chunk_size, low_memory=False)

    # Process each chunk and concatenate the results
    processed_chunks = []
    # Show progress bar by default
    if not hide_progress_bar:
        # Count total number of lines in the csv_file
        total_chunks = int(sum(1 for row in open(csv_file, "r")) / chunk_size)
        with alive_bar(
            total_chunks, force_tty=True, bar="filling", spinner="waves"
        ) as bar:
            bar.title = "Processing file -> " + csv_file
            for chunk in chunk_reader:
                processed_chunk = process_function(chunk, pf_args)
                processed_chunks.append(processed_chunk)
                bar()
    else:
        processed_chunk = process_function(chunk, pf_args)
        processed_chunks.append(processed_chunk)

    # Concatenate the processed chunks into a single DataFrame
    df = None
    # If the first chunk returned None then all returned None duh
    if processed_chunks[0] != None:
        df = pd.concat(processed_chunks, ignore_index=True)

    return df
