import os


async def createDirectory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
