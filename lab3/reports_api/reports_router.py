from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from report_service.reporter import ReportService

app = FastAPI()
report_service = ReportService()


class Report(BaseModel):
    title: str
    type: str
    text: str
    author_id: int


@app.post("/reports/")
def create_report(report: Report):
    report_id = report_service.create_report(
        report.title, report.type, report.text, report.author_id)
    return {"report_id": report_id}


@app.get("/reports/{report_id}")
def read_report(report_id: str):
    report = report_service.read_report(report_id)
    if report:
        return report
    else:
        raise HTTPException(status_code=404, detail="Отчет не найден")


@app.put("/reports/{report_id}")
def update_report(report_id: str, report: Report):
    if report_service.update_report(report_id, report.title, report.type, report.text, report.author_id):
        return {"message": "Отчет успешно обновлен"}
    else:
        raise HTTPException(status_code=404, detail="Отчет не найден")


@app.delete("/reports/{report_id}")
def delete_report(report_id: str):
    if report_service.delete_report(report_id):
        return {"message": "Отчет успешно удален"}
    else:
        raise HTTPException(status_code=404, detail="Отчет не найден")
