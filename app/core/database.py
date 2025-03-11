from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# DB configuration from .env file
DB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "thrones_db")

# Initialize MongoDB connection
client = MongoClient(DB_URI)
db = client[DB_NAME]
characters_collection = db["characters"]  # Collection für Charaktere
