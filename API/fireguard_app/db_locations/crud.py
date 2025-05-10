# Handles the database operations related to storing
# location and firerisk data
import datetime
from bson import ObjectId
from pymongo.collection import Collection


class LocationOperations:
    def __init__(self, collection: Collection):
        self.collection = collection

    def collection_exists(self, collection_name: str):
        try:
            collections = self.collection.database.list_collection_names()
            return collection_name in collections
        except Exception as e:
            print(f"An error occurred when checking if the collection exists: {e}")
        return False

    def create_location(self, location_data: dict):
        try:
            result = self.collection.insert_one(location_data)
        except Exception as e:
            print(f"An error occurred when trying to create a location: {e}")
            return None
        return result.inserted_id

    def get_location_by_name(self, location_name: str):
        try:
            location = self.collection.find_one({"name": location_name})
        except Exception as e:
            print(f"An error occurred when retriving a location by name: {e}")
            return None
        return location

    def get_location(self, location_id: str):
        try:
            location = self.collection.find_one({"_id": ObjectId(location_id)})
        except Exception as e:
            print(f"An error occurred when retrieving a location by id: {e}")
            return None
        return location

    def update_location_firerisk(self, name: str, fire_risk: str):
        try:
            self.collection.update_one({"name": name},
                                       {"$set": {"fireRiskPrediction": fire_risk,
                                        "lastModified": datetime.date.today().isoformat()}})
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        return True

    def delete_location(self, location_id: str):
        try:
            self.collection.delete_one({"_id": ObjectId(location_id)})
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        return True
