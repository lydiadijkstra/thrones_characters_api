import json


FILE_PATH = "characters.json"

def fetch_data():

    with open(FILE_PATH, "r", encoding="utf-8") as handle:
        characters = json.load(handle)
        return characters

print(fetch_data())