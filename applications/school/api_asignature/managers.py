from django.db import models


class AsignatureManager(models.Manager):

    def is_active(self, pk=None):
        asignature = None
        try:
            asignature = self.filter(id=None, auth_state='A').first()
        except:
            pass
        if asignature is None:
            return False

        return True

    def get_asignature_list(self):
        return self.select_related('knowledge_area').filter(auth_state='A').order_by('name')

    def get_asignature_by_id(self, pk=None):
        asignature = None
        try:
            asignature = self.select_related('knowledge_area').filter(id=pk, auth_state='A').first()
        except:
            pass
        return asignature
