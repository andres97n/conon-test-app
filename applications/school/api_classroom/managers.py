from django.db import models


class ClassroomManager(models.Manager):

    def get_classroom_list(self):
        return self.filter(auth_state='A').order_by('name')

    def get_classroom_by_id(self, pk=None):
        classroom = None
        try:
            classroom = self.filter(id=pk, auth_state='A').first()
        except:
            pass
        return classroom
