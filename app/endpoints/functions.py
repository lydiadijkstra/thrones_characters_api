from flask import request


def filtering(all_characters):
    filters = request.args

    # Dynamic filtering, lists only the characters where ALL filters are satisfied
    ## Example filtering age and strength: /filter?symbol=wolf&nickname=king in the north
    filtered_characters = []
    for character in all_characters:
        if all(str(character.get(key, "")).lower() == value.lower() for key, value in filters.items() if value):
            filtered_characters.append(character)

    return filtered_characters
