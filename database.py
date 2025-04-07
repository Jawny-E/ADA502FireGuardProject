import datetime
import os
from bson import ObjectId
from pymongo import MongoClient

# poetry self add poetry-plugin-dotenv@latest
# poetry lock
# poetry install
"""
# add the following to .env file
MONGO_DB_USERNAME = username
MONGO_DB_PASSWORD = password
MONGO_DB_URL = mongodb+srv://${MONGO_DB_USERNAME}:${MONGO_DB_PASSWORD}@fireguardproject.ggfqm.mongodb.net/
"""

MONGO_DB_URL = os.environ['MONGO_DB_URL']
client = MongoClient(MONGO_DB_URL)
db = client['FireGuardProject']


# Check if collection exists
def collection_exists(db, collection_name):
    try:
        # Attempt to list collection names
        collections = db.list_collection_names()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    return collection_name in collections


# Check if 'users' collection exists
if collection_exists(db, 'location'):
    location_collection = db['location']
else:
    print("The collection does not exist.")


def create_location(location_data):
    try:
        result = location_collection.insert_one(location_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return result.inserted_id


def get_location_by_name(location_name):
    try:
        location = location_collection.find_one({"name": location_name})
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return location


def get_location(location_id):
    try:
        location = location_collection.find_one({"_id": ObjectId(location_id)})
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return location


def update_location_firerisk(name, fire_risk):
    try:
        location_collection.update_one({"name": name},
                                       {"$set": {"fireRiskPrediction": fire_risk,
                                        "lastModified": datetime.date.today().isoformat()}})
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True


def delete_location(location_id):
    try:
        location_collection.delete_one({"_id": ObjectId(location_id)})
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True


create_location({
    "name": "Hjelmeland",
    "coordinates": {
        "latitude": 59.1302,
        "longitude": 6.2740
    },
    "fireRiskPrediction": None,
    "lastModified": None
})
