from fastapi import APIRouter

from app.routers import classes

app_router = APIRouter()

app_router.include_router(classes.router, prefix="/classes")
