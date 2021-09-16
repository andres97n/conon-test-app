from django.db import models


class StudentManager(models.Manager):

    def get_person_data(self, pk=None):
        student = None
        try:
            student = self.select_related('person').filter(id=pk).values(
                'person__identification',
                'person__name',
                'person__last_name',
                'person__gender',
                'person__phone'
            ).first()
        except:
            pass
        return student
