# Flask imports
from flask import Blueprint, jsonify, request


# Blueprint for possibility to have several endpoints
home_bp = Blueprint("home", __name__, url_prefix="/")


@home_bp.route("/", methods=["GET"])
def home():
    """
    Endpoint for fetching characters from the JSON file with pagination
    :return: Paginated list of characters
    """
    return "Homepage for characters of throne dingsda"
