from alive_progress import alive_bar
import pandas as pd

# Process any CSV file in chunks instead of whole file at once
async def processCSVInChunks(csv_file, chunk_size, process_function, pf_params):
    # Create a generator to read the CSV file in chunks
    chunk_reader = pd.read_csv(csv_file, chunksize=chunk_size)

    # Process each chunk and concatenate the results
    processed_chunks = []
    total_chunks = int(sum(1 for row in open(csv_file, "r")) / chunk_size)
    with alive_bar(total_chunks, force_tty=True, bar="filling", spinner="waves") as bar:
        bar.title = "Processing file -> " + csv_file
        for chunk in chunk_reader:
            processed_chunk = process_function(chunk, pf_params)
            processed_chunks.append(processed_chunk)
            bar()
    # Concatenate the processed chunks into a single DataFrame
    df = pd.concat(processed_chunks, ignore_index=True)

    return df