from pydantic import BaseModel as Model

class Student(Model):
    id: int
    class_id: int
    name: str
