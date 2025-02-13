import json
import os


BASE_DIR = os.path.dirname(__file__) # Creates the absolute path for usage from other dir
FILE_PATH = os.path.join(BASE_DIR, "characters.json")


def save_data(characters):
    """
    Overwrite the dictionary with the updated dictionary
    :param characters: dictionary
    :return: updated dictionary
    """
    with open(FILE_PATH, "w", encoding="utf-8") as handle:
        json.dump(characters, handle, indent=4)
