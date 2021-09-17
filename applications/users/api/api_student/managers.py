from django.db import models


class StudentManager(models.Manager):

    # Get Person data to a Student
    def get_person_data(self, pk=None):
        student = None
        try:
            student = self.select_related('person').filter(id=pk, auth_state='A').first()
        except:
            pass
        return student

    # Get Student List
    def get_student_list(self):
        students = self.select_related('person').filter(auth_state='A').order_by('person__last_name')
        return students
