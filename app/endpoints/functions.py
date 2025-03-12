from flask import request


def filtering(all_characters):
    """
    Filters the characters with the given filters.
    Example filtering age and strength: /filter?symbol=wolf&nickname=king in the north
    :param all_characters: list with all the available characters
    :return: the leftover characters after all used filters
    """
    print(f"Entering filter function wirh {len(all_characters)} characters")
    filters = request.args.to_dict() # convert into normal dict to pop sort and order
    filters.pop("sort_by", None)
    filters.pop("order", None)

    # Dynamic filtering, lists only the characters where ALL filters are satisfied
    filtered_characters = []
    for character in all_characters:
        if all(str(character.get(key, "")).lower() == value.lower() for key, value in filters.items() if value):
            filtered_characters.append(character)

    return filtered_characters


def sorting(filtered_characters):
    """
    Sorts characters based on sorting parameters.
    Example: /filter?sort_by=name&order=desc
    :param filtered_characters: list of characters
    :return: sorted characters
    """
    sort_by = request.args.get("sort_by", default=None, type=str)
    order = request.args.get("order", default="asc", type=str).lower()

    if not sort_by:
        return filtered_characters  # No sorting applied

    try:
        # Determine sorting type (numeric or string)
        first_value = next((char.get(sort_by) for char in filtered_characters if char.get(sort_by) is not None), None)

        if isinstance(first_value, (int, float)):
            sorted_characters = sorted(
                filtered_characters,
                key=lambda x: x.get(sort_by, float("-inf") if order == "desc" else float("inf")),
                reverse=(order == "desc")
            )
        else:
            sorted_characters = sorted(
                filtered_characters,
                key=lambda x: str(x.get(sort_by, "")).lower(),
                reverse=(order == "desc")
            )

        return sorted_characters

    except KeyError:
        print(f"Sorting error: Invalid sort key '{sort_by}'")
        return filtered_characters  # Return unsorted if the key doesn't exist

    except TypeError as e:
        print(f"Sorting error: {e}")
        return filtered_characters  # Return unsorted if there's a type mismatch
