from django.db import models


class TeacherManager(models.Manager):

    # Get Person data of the Teacher
    def get_teacher_person(self, pk=None):
        teacher = None
        try:
            teacher = self.select_related('person').filter(id=pk).values(
                'person__identification',
                'person__name',
                'person__last_name',
                'person__age',
                'person__phone'
            ).first()
        except:
            pass
        return teacher
