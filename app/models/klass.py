from app.models import Model

class Class(Model):
    __tablename__ = "classes"

    name: str
    subject: str
    course_code: str

class NewClass(Class):
    pass

class GetClass(Class):
    id: int
    students: str = None
