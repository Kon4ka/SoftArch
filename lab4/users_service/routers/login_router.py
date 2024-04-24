import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, HTTPException, Depends
import jwt
from utils.postgres_connector import PostgresConnector
import psycopg2
import hashlib

router = APIRouter()
connection = PostgresConnector(db_name="conference_db")

security = HTTPBasic()
SECRET_KEY = "secret_key"


@router.get("/auth")
def auth(token: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    current_user = payload["user"]
    sql_query = f"SELECT user_id FROM users \n"
    sql_query += f"WHERE users.user_login = %s"
    cursor.execute(sql_query, (current_user, ))
    result = cursor.fetchone()
    if result:
        return {"user_id": result[0], "user_name": current_user}
    return []


@router.get("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    if credentials.username and credentials.password:
        token = jwt.encode({'user': credentials.username, 'exp': datetime.datetime.now(
        ) + datetime.timedelta(minutes=30)}, SECRET_KEY, algorithm="HS256")
        sql_query = f"SELECT user_password FROM users \n"
        sql_query += f"WHERE users.user_login = %s"
        cursor.execute(sql_query, (credentials.username,))
        result = cursor.fetchone()
        cursor.close()
        if not result:
            return []
        hashed_password: str = hashlib.sha256(
            credentials.password.encode()).hexdigest()
        if hashed_password == result[0]:
            return {"token": token}
        else:
            return {"message": "Bad password"}
    elif credentials.username:
        return {"message": "Bad username"}
    else:
        return {"message": "Bad password"}
