# Flask imports
from flask import Blueprint, jsonify, request

# Random
from random import sample

# imports
from app.data.json_data_fetcher import fetch_data


# Blueprint for possibility to have several endpoints
characters_bp = Blueprint("characters", __name__, url_prefix="/characters")


@characters_bp.route("/", methods=["GET"])
def get_characters_data():
    """
    Endpoint for fetching characters from the JSON file with pagination
    :return: Paginated list of characters
    """
    characters = fetch_data()

    # Use slicing to slice from the number to skip until the limit, default limit 3
    limit = request.args.get("limit", default=20, type=int)
    skip = request.args.get("skip", default=0, type=int)

    # Pick a number of characters randomly from the list
    if limit and skip == 0:
        random_choice_of_characters = sample(characters, min(limit, len(characters)))
    else:
        # Paginate the list of characters
        paginated_characters = characters[skip : skip + limit]
        return paginated_characters
    return jsonify(random_choice_of_characters)


@characters_bp.route("/<int:id>", methods=["GET"])
def get_character_by_id(id):
    """
    Endpoint for fetching data for character with the matching id
    :param id:
    :return: json data of the character that fits the id
    """
    characters = fetch_data()

    # Loop through the list to find the matching character_id
    for character in characters:
        if character["id"] == id:
            return jsonify(character)

    return jsonify({"error": "Character not found"}), 404
