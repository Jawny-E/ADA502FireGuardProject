from fireguard_app.db_locations.crud import LocationOperations

import mongomock
import unittest


class TestLocationCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client = mongomock.MongoClient()
        cls.mock_db = cls.mock_client['MockDB']
        cls.mock_collection = cls.mock_db['location']

        cls.location_ops = LocationOperations(cls.mock_collection)

    def setUp(self):
        self.mock_collection.delete_many({})

    def test_create_and_get_location(self):
        data = {
            "name": "Hjelmeland",
            "coordinates": {
                "latitude": 59.1302,
                "longitude": 6.2740
            },
            "fireRiskPrediction": None,
            "lastModified": None
        }
        location_id = self.location_ops.create_location(data)
        self.assertIsNotNone(location_id)

        retrieved = self.location_ops.get_location(str(location_id))
        self.assertEqual(retrieved["name"], "Hjelmeland")

    def test_update_location_firerisk(self):
        location_id = self.mock_collection.insert_one({
            "name": "UpdateMe",
            "coordinates": {"latitude": 2.0, "longitude": 2.0},
            "fireRiskPrediction": None,
            "lastModified": None
        }).inserted_id

        updated = self.location_ops.update_location_firerisk("UpdateMe", "High")
        self.assertTrue(updated)

        updated_doc = self.mock_collection.find_one({"_id": location_id})
        self.assertEqual(updated_doc["fireRiskPrediction"], "High")
        self.assertIsNotNone(updated_doc["lastModified"])

    def test_delete_location(self):
        location_id = self.mock_collection.insert_one({
            "name": "DeleteMe",
            "coordinates": {"latitude": 3.0, "longitude": 3.0},
            "fireRiskPrediction": None,
            "lastModified": None
        }).inserted_id

        deleted = self.location_ops.delete_location(str(location_id))
        self.assertTrue(deleted)

        doc = self.mock_collection.find_one({"_id": location_id})
        self.assertIsNone(doc)

    def tearDown(self):
        self.mock_collection.delete_many({})
