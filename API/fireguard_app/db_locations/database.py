# Handles the connection to a cloud provisioned MongoDB database
from pymongo import MongoClient


class DatabaseClient:
    def __init__(
        self,
        username: str,
        password: str,
        cluster_url: str,
        database_name: str,
        collection_name: str
    ):
        self.mongo_url = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
