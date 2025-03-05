import json
import os


BASE_DIR = os.path.dirname(__file__) # Creates the absolute path for usage from other dir
FILE_PATH = os.path.join(BASE_DIR, "characters.json")

def fetch_data():
    """
    Opens the JSON-file characters.json.
    Converts JSON into Python-list
    :return: List with dicts, containing all the data of the characters
    """
    with open(FILE_PATH, "r", encoding="utf-8") as handle:
        characters = json.load(handle)
        return characters
