from pymongo import MongoClient
from pymongo.database import Database
import config 


client = MongoClient(config.MONGO_DB_URL)
db: Database = client.get_database(config.database_name)

# check db connection
if db is None:
    raise ValueError("Cannot connect to Database")
