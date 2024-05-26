from bson.objectid import ObjectId
from connector.mongo_connector import MongoDB


class ConferenceCRUD:
    def __init__(self):
        self.client = MongoDB().get_client()
        self.db = self.client["arch"]
        self.collection = self.db["conferences"]

    def read_all(self):
        response = []
        for i in self.collection.find():
            conf = {}
            conf['_id'] = str(i['_id'])
            conf['name'] = str(i["name"])
            response.append(conf)
        return response

    def create_conference(self, conference_data: dict):
        inserted_conference = self.collection.insert_one(conference_data)
        return str(inserted_conference.inserted_id)

    def read_conference(self, conference_id: str):
        conference = self.collection.find_one({"_id": ObjectId(conference_id)})
        if conference:
            conference['_id'] = str(conference['_id'])
            for i in range(len(conference['reports'])):
                conference['reports'][i] = str(conference['reports'][i])
        return conference

    def update_conference(self, conference_id: str, updated_data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(conference_id)},
            {"$set": updated_data}
        )
        return result.modified_count

    def delete_conference(self, conference_id: str):
        result = self.collection.delete_one({"_id": ObjectId(conference_id)})
        return result.deleted_count
