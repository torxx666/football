import pymongo
import json


class UsersManager:
    def __init__(self, db) -> None:
        self.db = db
        self.users_collection = "users"
        self.club_collection = "clubs"

    def get_user_list(self, user_ids, skip, limit) -> str:
        _collection_user = self.db[self.users_collection]

        liste_ids = list(map(int, user_ids.split(",")))

        pipeline = [
            {"$match": {"external_id": {"$in": liste_ids}}},
            {
                "$lookup": {
                    "from": self.club_collection,
                    "localField": "club",
                    "foreignField": "Club",
                    "as": "club_data",
                }
            },
            {"$unwind": "$club_data"},
            {
                "$addFields": {
                    "club_data.Country": "$club_data.Country",
                    "external_id": "$external_id",
                    "name": "$name",  #
                }
            },
            {
                "$group": {
                    "_id": "$club",
                    "club_data": {"$first": "$club_data"},
                    "external_id": {"$first": "$external_id"},
                    "name": {"$first": "$name"},
                }
            },
            {"$sort": {"_id": -1}},
        ]
        pipeline.append({"$skip": skip})
        pipeline.append({"$limit": limit})
        documents_filtres = _collection_user.aggregate(pipeline)

        export = []
        for document in documents_filtres:
            print(document)
            export.append(
                {
                    "user_id": document["external_id"],
                    "name": document["name"],
                    "club": document["_id"],
                    "club_country": document["club_data"]["Country"],
                    "Total": document["club_data"]["Total"],
                }
            )

        return export
