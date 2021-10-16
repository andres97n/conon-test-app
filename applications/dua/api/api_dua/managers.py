from django.db import models


class DuaManager(models.Manager):

    def get_dua_list(self):
        return self.select_related('topic').filter(auth_state='A').order_by('created_at')

    def get_dua_by_id(self, pk=None):
        dua = None
        try:
            dua = self.select_related('topic').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            pass
        return dua
