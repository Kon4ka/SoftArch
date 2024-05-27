from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
import hashlib
import requests
import pybreaker
from models.report_model import Report
import json

router = APIRouter()
security: HTTPBasicCredentials = HTTPBasic()
security_bearer = HTTPBearer()

# Create a Circuit Breaker instance
circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


def get_token(credentials: HTTPBasicCredentials):
    try:
        response = circuit_breaker.call(
            requests.get,
            "http://user_service:8080/api/login_router/login",
            auth=(credentials.username, credentials.password)
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()["token"]
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="User service unavailable due to Circuit Breaker")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Что то не так с токеном, возможно, его не существуе")


@router.get("/user_reports")
def get_report(user_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.get,
            f"http://reports:8080/user_reports?user_id={user_id}",
            headers=headers
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Reports service unavailable due to Circuit Breaker")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/get_report")
def get_report(report_id: str, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.get,
            f"http://reports:8080/reports_read?report_id={report_id}",
            headers=headers
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Reports service unavailable due to Circuit Breaker")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/create_report")
def create_report(report: Report, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.post,
            f"http://reports:8080/reports/",
            headers=headers,
            data=report.model_dump_json()
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Reports service unavailable due to Circuit Breaker")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.put("/update_report")
def update_report(report_id: str, report: Report, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.put,
            f"http://reports:8080/update_report?report_id={report_id}",
            headers=headers,
            data=report.model_dump_json()
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError as e:
        raise HTTPException(
            status_code=503, detail="Reports service unavailable due to Circuit Breaker")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.delete("/delete_report")
def delete_report(report_id: str, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.delete,
            f"http://reports:8080/reports_delete?report_id={report_id}",
            headers=headers
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Reports service unavailable due to Circuit Breaker")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
