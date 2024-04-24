from pydantic import BaseModel


class ReportModel(BaseModel):
    report_id: int
    report_title: str
    mongodb_id: str


class NewReportModel(BaseModel):
    report_title: str
    mongodb_id: str


class UpdateReportModel(BaseModel):
    report_id: int
    report_title: str | None = None
    mongodb_id: str | None = None
