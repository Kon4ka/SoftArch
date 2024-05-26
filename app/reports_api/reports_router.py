from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from report_service.reporter import ReportService
import redis
import json
import requests
import jwt

app = FastAPI()
report_service = ReportService()
r = redis.Redis(host='redis', port=6379, db=0)
SECRET_KEY = "secret_key"
security = HTTPBearer()


class Report(BaseModel):
    title: str
    type: str
    text: str
    author_id: int


def auth(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        current_user = payload["user_id"]
    except:
        raise HTTPException(
            status_code=401, detail="Invalid user data")
    return {"user_id": current_user}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        if error["msg"] == "Field required":
            modified_details.append(
                {
                    "message": f"The field {error["loc"][1]} absent in your request",
                }
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


@app.get("/user_reports")
def read_user_reports(user_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        author_id = auth(credentials.credentials)['user_id']
        print(type(author_id), type(user_id))
        if author_id != user_id:
            raise HTTPException(status_code=401, detail="Не тот аккаунт")
        reports = report_service.read_user_reports(user_id)
        if reports:
            return {"reports": reports}
        else:
            raise HTTPException(
                status_code=404, detail="Отчеты не найден")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Невалидный ID")


@ app.get("/reports_read")
def read_report(report_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        author_id = auth(credentials.credentials)['user_id']
        key = f'reports/{report_id}'
        redis_info = r.get(key)
        if redis_info:
            print("Redis info")
            redis_author_id = json.loads(redis_info)["author_id"]
            if redis_author_id == author_id:
                return {"report": json.loads(redis_info), "message": "Взято из redis"}
            else:
                raise HTTPException(status_code=400, detail="Не тот аккаунт")
        report = report_service.read_report(report_id)
        if report:
            if report["author_id"] == author_id:
                report_json = json.dumps(report)
                r.set(key, report_json)
                r.expire(key, 30)
                return {"report": report}
            else:
                raise HTTPException(status_code=401, detail="Не тот аккаунт")
        else:
            raise HTTPException(
                status_code=404, detail="Отчет не найден")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Невалидный ID")


@ app.post("/reports/")
def create_report(report: Report, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        author_id = auth(credentials.credentials)['user_id']
        if author_id == report.author_id:
            report_id = report_service.create_report(
                report.title, report.type, report.text, report.author_id)
            key = f'reports/{report_id}'
            report = report_service.read_report(report_id)
            json_report = json.dumps(report)
            if report:
                r.set(key, json_report)
                r.expire(key, 30)
                return report
        else:
            raise HTTPException(
                status_code=401, detail="Неверный аккаунт для создания")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Некорректный ввод или статья уже существует в БД")
    return {"report_id": report_id}


@ app.put("/update_report")
def update_report(report_id: str, report: Report, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if auth(credentials.credentials)['user_id'] == report.author_id:
            updated_report = report_service.update_report(
                report_id, report.title, report.type, report.text, report.author_id)
        else:
            raise HTTPException(
                status_code=401, detail="Невалидный id автора для зименения")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Невалидный id")
    if updated_report and updated_report != 1:
        key = f'reports/{report_id}'
        updated_report_json = json.dumps(updated_report)
        r.rpush(key, updated_report_json)
        r.expire(key, 30)
        return updated_report
    elif updated_report == 1:
        raise HTTPException(
            status_code=400, detail="Нечего обновлять")
    else:
        raise HTTPException(
            status_code=400, detail="Ничего нет по данному id")


@ app.delete("/reports_delete")
def delete_report(report_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        report_info = requests.get(
            f"http://reports:8080/reports_read?report_id={report_id}", headers=headers)
        if report_info.status_code == 200:
            author_id = auth(credentials.credentials)['user_id']
            print(report_info.json())
            if report_info.json()["report"]["author_id"] == author_id:
                key = f'deleted/{report_id}'
                redis_info = r.get(key)
                if redis_info:
                    return {"message": json.loads(redis_info)}
                if report_service.delete_report(report_id):
                    r.set(key, "Отчет не найден (использован redis)")
                    r.expire(key, 100)
                    return {"message": "Отчет успешно удален"}
                else:
                    raise HTTPException(
                        status_code=404, detail="Отчет не найден")
            else:
                raise HTTPException(
                    status_code=401, detail="Некорректный аккаунт")
        elif report_info.status_code == 404:
            raise HTTPException(
                status_code=404, detail="Отчет не найден")
        else:
            raise HTTPException(
                status_code=401, detail="Некорректный аккаунт")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Некорректная информация")
