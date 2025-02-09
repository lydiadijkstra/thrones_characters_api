from flask import Flask, jsonify, request

from app.core.database import initialize_database

app = Flask(__name__)


def create_app():
    """
    Initialize the storage and the app.
    Run the app.
    """
    app = Flask(__name__)
    initialize_database()

    print("Welcome at my Game of Thrones Character API")

    #return app


if __name__ == "__main__":
    create_app()