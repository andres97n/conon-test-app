from django.db import models


class GlosaryManager(models.Manager):

    def get_glosary_list(self):
        return self.select_related('asignature_classroom').\
            filter(auth_state='A').order_by('created_at')

    def get_glosary_by_id(self, pk=None):
        glosary = None
        try:
            glosary = self.select_related('asignature_classroom').\
                filter(id=pk, auth_state='A').first()
        except None:
            pass
        return glosary

    def glosary_exists(self, pk=None):
        glosary = None
        try:
            glosary = self.filter(id=pk, auth_state='A').first()
        except None:
            pass

        if glosary is None:
            return False

        return True