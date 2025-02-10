from flask import Blueprint, jsonify

from app.data.json_data_fetcher import fetch_data
#from app.main.py import app


characters_bp = Blueprint("characters", __name__)

CHARACTERS = fetch_data()

@characters_bp.route("/characters", methods=["GET"])
def get_characters_data():
    """
    Endpoint for fetching Data from the JSON file
    :return: Characters Data
    """
    return jsonify(CHARACTERS)
