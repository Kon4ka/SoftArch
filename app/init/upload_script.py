from postgres_connector import PostgresConnector
from faker import Faker
from typing import Sequence, Mapping
import hashlib
import random
import psycopg2.extras


class DBWorker:
    def create_new_db(self, db_name: str) -> None:
        connector: PostgresConnector = PostgresConnector()
        cursor = connector.get_cursor()
        cursor.connection.autocommit = True
        drop_command = f"DROP DATABASE IF EXISTS {db_name};"
        creation_command = f"CREATE DATABASE {db_name};"
        cursor.execute(drop_command)
        cursor.execute(creation_command)
        connector.close_connection()

    def create_tables(self, db_name: str) -> None:
        connector: PostgresConnector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        with open("./sql_script.sql", "r") as tables_creation_cript:
            cursor.execute(tables_creation_cript.read())
        cursor.connection.commit()
        connector.close_connection()

    def insert_data_to_table(self, db_name: str, table_name: str, data: Sequence[Mapping]) -> None:
        connector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        columns = data[0].keys()
        columns_str = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES %s"
        data_to_insert = [[i[column] for column in columns] for i in data]
        psycopg2.extras.execute_values(cursor, sql, data_to_insert)
        cursor.connection.commit()
        connector.close_connection()


class CreaterData:
    def get_fake_users(self, count: int) -> Sequence[Mapping]:
        fake: Faker = Faker()
        users: Sequence[Mapping] = []
        for _ in range(count):
            user = self.create_fake_user(fake)
            users.append(user)
        return users

    def create_fake_user(self, fake: Faker) -> Mapping:
        user: dict = {}
        user_login: str = fake.unique.user_name()
        full_name: Sequence[str] = fake.unique.name().split()[:2]
        user_name: str = full_name[0]
        user_surname: str = full_name[1]
        password: str = fake.unique.password()
        user_password: str = hashlib.sha256(password.encode()).hexdigest()
        user["user_login"] = user_login
        user["user_name"] = user_name
        user["user_surname"] = user_surname
        user["user_password"] = user_password
        return user

    def get_fake_reports(self, count: int) -> Sequence[Mapping]:
        fake: Faker = Faker()
        reports: Sequence[Mapping] = []
        for _ in range(count):
            report = {
                "report_title": fake.unique.company(),
                "mongodb_id": fake.unique.sbn9(),
            }
            reports.append(report)
        return reports

    def get_fake_conferences(self, count: int) -> Sequence[Mapping]:
        fake: Faker = Faker()
        conferences: Sequence[Mapping] = []
        for _ in range(count):
            day: int = random.randint(1, 30)
            month: int = random.randint(1, 12)
            year: str = str(random.randint(2010, 2023))
            day_str = str(day) if day > 9 else '0' + str(day)
            month_str = str(month) if month > 9 else '0' + str(month)
            conference_date = int(year + month_str + day_str)
            conference = {
                "conference_name": fake.unique.company(),
                "conference_date": conference_date,
                "conference_description": fake.unique.text()
            }
            conferences.append(conference)
        return conferences


class Uploader:
    def upload_data(self):
        print("Start initializing")
        cursor = PostgresConnector().get_cursor()
        sql = "SELECT datname FROM pg_database WHERE datname = 'conference_db'"
        cursor.execute(sql)
        if cursor.fetchall():
            print("Database already exist")
            cursor.close()
            return
        cursor.close()
        db_worker = DBWorker()
        db_name = "conference_db"
        creater_data = CreaterData()
        db_worker.create_new_db(db_name)
        db_worker.create_tables(db_name)
        fake_users: Sequence[Mapping] = creater_data.get_fake_users(10)
        fake_reports: Sequence[Mapping] = creater_data.get_fake_reports(10)
        fake_conferences: Sequence[Mapping] = creater_data.get_fake_conferences(
            10)
        db_worker.insert_data_to_table(
            db_name=db_name, table_name="users", data=fake_users)
        db_worker.insert_data_to_table(
            db_name=db_name, table_name="reports", data=fake_reports)
        db_worker.insert_data_to_table(
            db_name=db_name, table_name="conferences", data=fake_conferences)
        print("Database was created and filled")


if __name__ == "__main__":
    Uploader().upload_data()
