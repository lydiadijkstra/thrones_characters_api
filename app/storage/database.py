import json
import os
from pymongo import MongoClient


# Connect to the local MongoDB
client = MongoClient("mongodb://localhost:27017")

# Create the Database
db = client["thrones_db"]
characters_collection = db["characters"]
