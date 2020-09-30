from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException

from app.models.student import Student, GetStudent

router = APIRouter()

@router.get("", response_model=List[GetStudent], response_model_exclude=["id", "class_id"])
def list_students():
    students = [GetStudent(**student.dict()) for student in Student.all()]

    return students


@router.get("/{id}", response_model=GetStudent, response_model_exclude=["id", "class_id"])
def get_student(id: int):
    student = Student.one(id=id)

    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {id} not found")

    student = GetStudent(**student.dict())

    return student
