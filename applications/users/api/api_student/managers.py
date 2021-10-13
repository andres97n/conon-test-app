from django.db import models


class StudentManager(models.Manager):

    def get_representative(self):
        return f'{self.representative_name} - {self.emergency_contact}'

    def mapper(self):
        return dict(
            id=self.id,
            name=self.person.name,
            last_name=self.person.last_name,
            identification=self.person.identification,
            expectations=self.expectations,
            phone=self.person.phone,
            representative=self.get_representative()
        )

    # Get Person data to a Student
    def get_student_detail_data(self, pk=None):
        student = None
        try:
            student = self.select_related('person').filter(id=pk, auth_state='A').first()
        except None:
            pass

        return student

    # Get Student List
    def get_student_list(self):
        students = self.select_related('person').filter(auth_state='A').order_by('person__last_name')
        return students

    def is_active(self, pk=None):
        student = None
        try:
            student = self.filter(id=pk, auth_state='A').first()
        except None:
            pass
        if student is None:
            return False

        return True
