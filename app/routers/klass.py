from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException

from app import app

from app.models.klass import Class, NewClass, GetClass
from app.models.student import Student, NewStudent, GetStudent

router = APIRouter()


@router.get("", response_model=List[GetClass], response_model_exclude=["id"])
def list_classes():
    classes = [GetClass(**klass.dict()) for klass in Class.all()]

    return classes


@router.get("/{id}", response_model=GetClass, response_model_exclude=["id"])
def get_class(id: int):
    klass = GetClass(**Class.one(id=id).dict())

    return klass


@router.post("", response_model=GetClass, response_model_exclude=["id"], status_code=status.HTTP_201_CREATED)
def create_class(klass: NewClass):
    new_class = Class.new(**klass.dict())

    return GetClass(**new_class.dict())


@router.post("/{id}/students", response_model=GetStudent, response_model_exclude=["id"], status_code=status.HTTP_201_CREATED)
def create_student(id: int, student: NewStudent):
    params = student.dict()
    params.update({"class_id": id})

    new_student = Student.new(**params)

    return GetStudent(**new_student.dict())


@router.get("/{id}/students", response_model=List[GetStudent], response_model_exclude=["id", "class_id"])
def list_students_for_class(id: int):
    students = Student.all(class_id=id)

    if len(students) == 0:
        raise HTTPException(status_code=404, detail=f"No students found for class {id}")

    # convert to a list of GetStudent objects
    students = [GetStudent(**student.dict()) for student in students]

    return students
