from typing import List

from fastapi import APIRouter
from fastapi import status

from app.models.klass import Class, NewClass, GetClass

router = APIRouter()

@router.get("", response_model=List[GetClass], response_model_exclude=["id"])
def index():
    return {"classes": Class.all()}


@router.get("/{id}", response_model=GetClass, response_model_exclude=["id"])
def get(id: int):
    klass = Class.one(id=id)

    return klass


@router.post("", response_model=GetClass, response_model_exclude=["id"], status_code=status.HTTP_201_CREATED)
def new(klass: NewClass):
    new_class = Class.new(**klass.dict())

    return new_class
