from django.db import models


class AsignatureClassroomManager(models.Manager):

    def get_asignature_classroom_list(self):
        return self.select_related(
            'classroom',
            'asignature',
            'teacher'
        ).filter(auth_state='A').order_by('classroom__name')

    def get_asignature_classroom_by_id(self, pk=None):
        asignature_classroom = None
        try:
            asignature_classroom = self.select_related(
                'classroom',
                'asignature',
                'teacher'
            ).filter(id=pk, auth_state='A').first()
        except:
            pass
        return asignature_classroom
