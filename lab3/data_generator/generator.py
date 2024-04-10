from pymongo import MongoClient
from faker import Faker

username = "root"
password = "example"
mongo_uri = f"mongodb://{username}:{password}@mongo:27017/"
client = MongoClient(mongo_uri)
db = client["arch"]
conferences_collection = db["conferences"]
reports_collection = db["reports"]
fake = Faker()


def generate_fake_report():
    reports = []
    count = fake.unique.random_int(min=100, max=1000)
    for _ in range(count):
        title = fake.unique.sentence()
        report_type = fake.word()
        text = fake.unique.paragraph()
        author_id = fake.random_int(min=1, max=1000000)
        reports.append(
            {
                "title": title,
                "type": report_type,
                "text": text,
                "author_id": author_id
            }
        )
    return reports


def generate_fake_conference():
    count_of_confs: int = fake.unique.random_int(min=20, max=30)
    confs = []
    for _ in range(count_of_confs):
        name = fake.unique.company()
        report_ids = reports_collection.insert_many(
            generate_fake_report()).inserted_ids
        date_of_conference = fake.unique.random_int(min=1, max=100)
        max_authors = fake.unique.random_int(min=1, max=100)
        confs.append(
            {
                "name": name,
                "reports": report_ids,
                "date_of_conference": date_of_conference,
                "max_authors": max_authors
            }
        )

    conferences_collection.insert_many(confs)
