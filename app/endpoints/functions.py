from pydoc import describe

from flask import request


def filtering(all_characters):
    """
    Filters the characters with the given filters.
    Example filtering age and strength: /filter?symbol=wolf&nickname=king in the north
    :param all_characters: list with all the available characters
    :return: the leftover characters after all used filters
    """
    filters = request.args

    # Dynamic filtering, lists only the characters where ALL filters are satisfied
    filtered_characters = []
    for character in all_characters:
        if all(str(character.get(key, "")).lower() == value.lower() for key, value in filters.items() if value):
            filtered_characters.append(character)

    return filtered_characters


def sorting(filtered_characters):
    """
    Sorts characters based on sorting parameters.
    Example: /?sort_by=name&order=desc
    :param filtered_characters: all the available characters
    :return: sorted characters based on sorting parameters
    """
    sort_by = request.args.get("sort_by", default=None, type=str)
    order = request.args.get("order", default="asc", type=str).lower()

    if sort_by:
        try:
            # Check if the sort_by key exists in the characters
            if not all(sort_by in character for character in filtered_characters):
                print(f"Field '{sort_by}' not found in some characters.")  # Debugging output
                return filtered_characters  # Return unmodified list if key is missing in any character

            # Determine if sorting should be numeric or string-based
            first_value = next((char.get(sort_by) for char in filtered_characters if sort_by in char), None)

            if isinstance(first_value, (int, float)):  # Sort numerically if possible
                sorted_characters = sorted(filtered_characters, key=lambda x: x.get(sort_by, 0), reverse=(order == "desc"))
            else:
                sorted_characters = sorted(filtered_characters, key=lambda x: str(x.get(sort_by, "")).lower(), reverse=(order == "desc"))

            return sorted_characters

        except Exception as e:
            print(f"Sorting error: {e}")  # Debugging output
            return filtered_characters  # Fail gracefully

    return filtered_characters
