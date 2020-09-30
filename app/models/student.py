from app.models import Model

class Student(Model):
    __tablename__ = "students"

    id: int = None
    uri: str = None
    name: str
    class_id: int = None

    def __init__(self, **params):
        Model.__init__(self, **params)

        if self.class_id:
            self.uri = self.get_link("get_student", id=self.id)

class NewStudent(Student):
    pass

class GetStudent(Student):
    klass: str = None

    def __init__(self, **params):
        Student.__init__(self, **params)

        self.klass = self.get_link("get_class", id=self.class_id)
