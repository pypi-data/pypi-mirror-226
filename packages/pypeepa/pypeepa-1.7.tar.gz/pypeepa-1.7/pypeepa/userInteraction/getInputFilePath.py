import os


async def getInputFilePath():
    while True:
        file_path = input(
            "Enter the path to the file containing the data. (Should be a .xlsx,.csv or .json file)\nPath to your file: "
        )
        file_path = await sanitizeFilePath(file_path)
        if file_path.endswith((".xlsx", ".csv", ".json")):
            return file_path
        else:
            print("Not a csv or xlsx file!")


async def sanitizeFilePath(user_input):
    # Remove leading/trailing whitespaces and quotes from the user input
    user_input = user_input.strip(" '\"")

    # Replace backslashes with forward slashes (for cross-platform compatibility)
    user_input = user_input.replace("\\", "/")

    # Remove any leading './' from the path
    if user_input.startswith("./"):
        user_input = user_input[2:]

    # Get the absolute path to handle relative paths
    sanitized_path = os.path.abspath(user_input)

    return sanitized_path
