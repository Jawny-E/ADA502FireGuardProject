# Handles the connection to a cloud provisioned MongoDB database
from pymongo import MongoClient


class DatabaseClient:
    def __init__(
        self,
        username: str,
        password: str,
        cluster_url: str,
        database_name: str
    ):
        self.database_name = database_name
        self.mongo_url = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
        self.client = MongoClient(self.mongo_url)

    def get_database(self):
        return self.client[self.database_name]

    def get_collection(self, name: str):
        return self.get_database()[name]
