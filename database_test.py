from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb+srv://[USERNAME:PASSWORD]@fireguardproject.ggfqm.mongodb.net/')
db = client['sample_mflix']
# Check if 'users' collection exists
def collection_exists(db, collection_name):
    try:
        # Attempt to list collection names
        collections = db.list_collection_names()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    return collection_name in collections

# Check if 'users' collection exists
if collection_exists(db, 'users'):
    users_collection = db['users']
    print("The 'users' collection exists.")
else:
    print("The 'users' collection does not exist.")



def create_user(user_data):
    result = users_collection.insert_one(user_data)
    return result.inserted_id

def get_user(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})


user = get_user("59b99db4cfa9a34dcd7885b7")

print(user.get("name"))
    
