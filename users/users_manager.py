import pymongo


class UsersManager:
    def __init__(self,db) -> None:
        self.db = db
        self.collection_name = "users"

    def get_user_list(self, skip, limit)-> str:
        collection = self.db[self.collection_name]

        # Find the last 10 documents in the collection
        cursor = collection.find().sort("_id", pymongo.DESCENDING).limit(10)

        # Iterate over the results
        for document in cursor:
            print(document)
        return {"ok"}
