from fastapi import APIRouter

from app.routers import klass, student

app_router = APIRouter()

app_router.include_router(klass.router, prefix="/classes")
app_router.include_router(student.router, prefix="/students")
