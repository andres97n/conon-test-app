from django.db import models


class TeacherManager(models.Manager):

    # Get Person data of the Teacher
    def get_person_data(self, pk=None):
        teacher = None
        try:
            teacher = self.select_related('person').filter(id=pk, auth_state='A').first()
        except:
            pass
        return teacher

    # Get Active Teacher List
    def get_teacher_list(self):
        teachers = self.select_related('person').filter(auth_state='A').order_by('person__last_name')
        return teachers

    # Return if the Teacher is active
    def is_active(self, pk=None):
        teacher = None
        try:
            teacher = self.filter(id=pk, auth_state='A').first()
        except:
            pass
        if teacher is None:
            return False

        return True
