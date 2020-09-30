from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException

from app import app

from app.models.klass import Class, NewClass, GetClass, UpdateClass
from app.models.student import Student, NewStudent, GetStudent

router = APIRouter()


# POST /api/v1/classes
@router.post("", response_model=GetClass, response_model_exclude=["id"], status_code=status.HTTP_201_CREATED, tags=["Class"])
def create_class(klass: NewClass):
    new_class = Class.new(**klass.dict())

    return GetClass(**new_class.dict())


# GET /api/v1/classes
@router.get("", response_model=List[GetClass], response_model_exclude=["id"], tags=["Class"])
def list_classes():
    classes = [GetClass(**klass.dict()) for klass in Class.all()]

    return classes


# GET /api/v1/classes/{id}
@router.get("/{id}", response_model=GetClass, response_model_exclude=["id"], tags=["Class"])
def get_class(id: int):
    klass = GetClass(**Class.one(id=id).dict())

    return klass


# PATCH /api/v1/classes/{id}
@router.patch("/{id}", response_model=GetClass, response_model_exclude=["id"], tags=["Class"])
def update_class(id: int, update: UpdateClass):
    klass = Class.one(id=id)

    klass.name = update.name or klass.name
    klass.subject = update.subject or klass.subject
    klass.course_code = update.course_code or klass.course_code

    klass.save()

    return GetClass(**klass.dict())


# POST /api/v1/classes/{id}/students
@router.post("/{id}/students", response_model=GetStudent, response_model_exclude=["id"], status_code=status.HTTP_201_CREATED, tags=["Class", "Student"])
def create_student(id: int, student: NewStudent):
    params = student.dict()
    params.update({"class_id": id})

    new_student = Student.new(**params)

    return GetStudent(**new_student.dict())


# GET /api/v1/classes/{id}/students
@router.get("/{id}/students", response_model=List[GetStudent], response_model_exclude=["id", "class_id"], tags=["Class", "Student"])
def list_students_for_class(id: int):
    students = Student.all(class_id=id)

    if len(students) == 0:
        raise HTTPException(status_code=404, detail=f"No students found for class {id}")

    students = [GetStudent(**student.dict()) for student in students]

    return students
