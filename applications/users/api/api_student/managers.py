from django.db import models


class StudentManager(models.Manager):

    def get_person_data(self):
        student = self.select_related('person').get(id=self.id)
        return dict(
            identification=student.person.identification,
            name=student.person.name,
            last_name=student.person.last_name,
            gender=student.person.gender,
            contact=student.person.phone
        )
