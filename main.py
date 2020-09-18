from typing import Optional, List

from fastapi import FastAPI

db = {
    "classes": [
        {
            "id": 1,
            "name": "Potions",
            "course_code": "POT20"
        },
        {
            "id": 2,
            "name": "Transfiguration",
            "course_code": "TRF23"
        },
    ],
    "students": [
        {
            "id": 13,
            "class_id": 1,
            "name": "Neville Longbottom"
        },
        {
            "id": 14,
            "class_id": 1,
            "name": "Draco Malfoy"
        },
        {
            "id": 15,
            "class_id": 1,
            "name": "Hannah Abbott"
        },
        {
            "id": 16,
            "class_id": 1,
            "name": "Cho Chang"
        },
        {
            "id": 24,
            "class_id": 2,
            "name": "Hermione Granger"
        },
        {
            "id": 25,
            "class_id": 2,
            "name": "Ronald Weasley"
        },
        {
            "id": 26,
            "class_id": 2,
            "name": "Harry Potter"
        },
    ]
}

from app import app

# app = FastAPI()

# @app.get("/api/v1/classes/{class_id}/students", response_model=List[Student])
# def list_students(class_id: int):
#     return list(filter(lambda student: student["class_id"] == class_id, db["students"]))


# @app.get("/api/v1/classes", response_model=List[Class])
# async def list_classes():
#     classes = [Class(**c) for c in db["classes"]]

#     for c in classes:
#         c.students = app.url_path_for("list_students", class_id=c.id)
#         # = f"/api/v1/classes/{c.id}/students"

#     return classes
