from bson.objectid import ObjectId
from connector.mongo_connector import MongoDB


class ReportService:

    def __init__(self):
        self.client = MongoDB().get_client()
        self.db = self.client["arch"]
        self.collection = self.db["reports"]

    def create_report(self, title, type, text, author_id):
        report_data = {
            "title": title,
            "type": type,
            "text": text,
            "author_id": author_id
        }
        result = self.collection.insert_one(report_data)
        return str(result.inserted_id)

    def read_report(self, report_id):
        report = self.collection.find_one({"_id": ObjectId(report_id)})
        if report:
            report['_id'] = str(report['_id'])
        return report

    def update_report(self, report_id, title=None, type=None, text=None, author_id=None):
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if type is not None:
            update_data["type"] = type
        if text is not None:
            update_data["text"] = text
        if author_id is not None:
            update_data["author_id"] = author_id

        result = self.collection.update_one(
            {"_id": ObjectId(report_id)}, {"$set": update_data})
        return result.modified_count > 0

    def delete_report(self, report_id):
        result = self.collection.delete_one({"_id": ObjectId(report_id)})
        return result.deleted_count > 0
