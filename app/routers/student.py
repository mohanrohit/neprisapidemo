from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Response
from fastapi import HTTPException

from app.models.student import Student, GetStudent, UpdateStudent

router = APIRouter()

# GET /api/v1/students
@router.get("", response_model=List[GetStudent], response_model_exclude=["id", "class_id"], tags=["Student"])
def list_students():
    students = [GetStudent(**student.dict()) for student in Student.all()]

    return students


# GET /api/v1/students/{id}
@router.get("/{id}", response_model=GetStudent, response_model_exclude=["id", "class_id"], tags=["Student"])
def get_student(id: int):
    student = Student.one(id=id)

    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {id} was not found")

    student = GetStudent(**student.dict())

    return student


# PATCH /api/v1/students/{id}
@router.patch("/{id}", response_model=GetStudent, response_model_exclude=["id", "class_id"], tags=["Student"])
def update_student(id: int, update: UpdateStudent):
    student = Student.one(id=id)

    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {id} was not found")

    student.name = update.name or student.name

    student.save()

    return GetStudent(**student.dict())


# DELETE /api/v1/students/{id}
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Student"])
def delete_student(id: int, response: Response):
    student = Student.one(id=id)

    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {id} was not found")

    student.delete()

    response.status_code = status.HTTP_204_NO_CONTENT

    return {}
