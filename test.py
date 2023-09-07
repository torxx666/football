import pymongo

# Replace these with your MongoDB connection details
USERNAME="de-assignment"

PASSWORD = "ZxULbW7O3wPs0Gpi"

mongo_uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@aui-de-assignments.cohiy.mongodb.net"  # MongoDB URI
database_name = "football_assignment"  # Name of the database

# Create a MongoDB client
client = pymongo.MongoClient(mongo_uri)

# Access the database
db = client[database_name]

# Now you can work with the database, for example, creating a collection and inserting data
collection_name = "users"  # Name of the collection


# Create a MongoDB client
client = pymongo.MongoClient(mongo_uri)

# Access the database
db = client[database_name]
# Obtenez la liste des collections (tables)
collections = db.list_collection_names()

# Parcourez et imprimez la liste des collections
for collection in collections:
    print(collection)

# Access the collection
collection = db[collection_name]

# Find the last 10 documents in the collection
cursor = collection.find().sort("_id", pymongo.DESCENDING).limit(10)

# Iterate over the results
for document in cursor:
    print(document)

# Close the MongoDB connection when you're done
client.close()