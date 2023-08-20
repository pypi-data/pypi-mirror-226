import os
from typing import List


async def asyncListDir(input_dir: str) -> List[str]:
    input_files = []
    for file_path in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, file_path)):
            input_files.append(file_path)
    return input_files
