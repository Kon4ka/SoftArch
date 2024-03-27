from fastapi import APIRouter, Depends
from utils.postgres_connector import PostgresConnector
import psycopg2
from models.report_model import NewReportModel

router = APIRouter()

connection = PostgresConnector(db_name="conference_db")


@router.get("/")
async def get_all_reports(cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_command: str = "SELECT * FROM reports"
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result


@router.post("/new_report")
async def new_report(new_report: NewReportModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        sql_command: str = "INSERT INTO reports (report_title, mongodb_id) VALUES (%s, %s)"
        data: tuple = (new_report.report_title, new_report.mongodb_id)
        cursor.execute(sql_command, data)
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        return {"message": "Report created unsuccessfully"}

    return {"message": "Report created successfully"}


@router.get("/add_report_to_conference")
async def add_report_to_conference(conference_id: int, report_id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        sql_command: str = "INSERT INTO conferences_reports (conference_id, report_id) VALUES (%s, %s)"
        data: tuple = (conference_id, report_id)
        cursor.execute(sql_command, data)
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        return {"message": "Report created unsuccessfully"}
    return {"message": "Report successfully added to conference"}


@router.get("/get_reports_by_conference")
async def get_reports_by_conference(conference_id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_command: str = "SELECT reports.report_id, reports.report_title, reports.mongodb_id from reports "\
        "JOIN conferences_reports ON conferences_reports.report_id=reports.report_id "\
        "where conference_id=%s;"
    data: tuple = (conference_id,)
    cursor.execute(sql_command, data)
    result = cursor.fetchall()
    return result


@router.delete("/delete")
async def delete_user(id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    tuple_id: tuple = (id,)
    sql_command = "DELETE FROM users WHERE user_id=%s"
    cursor.execute(sql_command, tuple_id)
    cursor.connection.commit()
    return {"message": "Report deleted successfully"}
