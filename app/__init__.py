import sqlite3

from fastapi import FastAPI

app = FastAPI()

def get_db():
    db = sqlite3.connect("db/students.db")
    db.row_factory = sqlite3.Row

    return db


from app import routers

app.include_router(routers.app_router, prefix="/api/v1")
print(app.routes)
