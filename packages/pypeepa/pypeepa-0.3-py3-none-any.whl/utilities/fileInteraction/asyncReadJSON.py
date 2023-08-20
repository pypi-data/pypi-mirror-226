import json


async def asyncReadJSON(file_name):
    read_data = []
    try:
        with open(file_name, "r") as openfile:
            read_data = json.load(openfile)
    except:
        print(f"Error reading JSON file {file_name}")
    return read_data
