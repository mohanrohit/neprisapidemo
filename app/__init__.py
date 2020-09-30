import sqlite3
import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

def get_db():
    db = sqlite3.connect("db/students.db")
    db.row_factory = sqlite3.Row
    db.set_trace_callback(print)

    return db


def get_app():
    return app


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


@app.get("/routes")
def index():
    routes = []

    for route in app.routes:
        method = [m for m in route.methods if m in ["GET", "POST", "PUT", "PATCH", "DELETE"]][0]

        routes.append(f"{method} {route.path}")

    return {"routes": routes}


app.include_router(routers.app_router, prefix="/api/v1")
