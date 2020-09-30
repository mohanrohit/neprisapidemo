import sqlite3
import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

tags = [
    { "name": "Class", "description": "Operations with the `Class` resource" },
    { "name": "Student", "description": "Operations with the `Student` resource" }
]

app = FastAPI(title="Nepris API Demo", openapi_tags=tags)

def get_db():
    db = sqlite3.connect("db/students.db")
    db.row_factory = sqlite3.Row
    db.set_trace_callback(print)

    return db


from app import routers

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        {
            "code": exc.status_code,
            "message": str(exc.detail)
        },
        status_code=exc.status_code
    )


@app.get("/", tags=["Default"])
def index():
    routes = []

    for route in app.routes:
        method = [m for m in route.methods if m in ["GET", "POST", "PUT", "PATCH", "DELETE"]][0]

        routes.append(f"{method} {route.path}")

    return {"routes": routes}


app.include_router(routers.app_router, prefix="/api/v1")
