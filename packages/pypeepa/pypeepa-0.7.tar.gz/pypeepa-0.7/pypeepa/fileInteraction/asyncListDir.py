import os
from typing import List


async def asyncListDir(
    dir: str, getFolders: bool = True, getFiles: bool = True
) -> List[str]:
    content = []
    for content_path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, content_path)) and getFiles is True:
            content.append(content_path)
        if os.path.isdir(os.path.join(dir, content_path)) and getFolders is True:
            content.append(content_path)
    return content
