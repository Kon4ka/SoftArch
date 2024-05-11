
from fastapi import FastAPI
from routers.user_router import router as user_router
from routers.reports_router import router as report_router

app = FastAPI()

app.include_router(user_router, tags=["Users"], prefix="/api/users")
app.include_router(report_router, tags=["Reports"], prefix="/api/reports")
