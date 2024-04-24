
from fastapi import FastAPI
from routers.user_router import router as user_router
from routers.login_router import router as login_router
app = FastAPI()

app.include_router(user_router, tags=["Users"], prefix="/api/users")
app.include_router(login_router, tags=["Login"], prefix="/api/login_router")
