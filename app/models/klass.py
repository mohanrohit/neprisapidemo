from app.models import Model

class Class(Model):
    __tablename__ = "classes"

    id: int = None
    uri: str = None
    name: str
    subject: str
    course_code: str

    def __init__(self, **params):
        Model.__init__(self, **params)

        self.uri = self.get_link("get_class", id=self.id)


    def get_students_link(self):
        return self.get_link("list_students", class_id=self.id)


class NewClass(Class):
    pass

class GetClass(Class):
    students: str = None

    def __init__(self, **params):
        Class.__init__(self, **params)

        self.students = self.get_link("list_students_for_class", id=self.id)

class UpdateClass(Class):
    name: str = None
    subject: str = None
    course_code: str = None
