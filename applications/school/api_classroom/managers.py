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

    def is_active(self, pk=None):
        classroom = None
        try:
            classroom = self.select_related('school_period').filter(
                id=pk,
                auth_state='A',
                school_period__state=1
            ).first()
        except:
            pass
        if classroom is None:
            return False
        else:
            return True
