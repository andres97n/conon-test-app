
from django.db import models


class RubricAcManager(models.Manager):

    def get_rubric_ac_active_queryset(self):
        return self.select_related('ac').filter(state=1, auth_state='A')

    def get_rubric_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('ac').filter(id=pk, state=1, auth_state='A')
        except:
            return None

    def get_rubric_ac_list(self):
        return self.get_rubric_ac_active_queryset().order_by('-created_at')

    def exists_rubric_ac(self, pk=None):
        return self.filter(id=pk, state=1, auth_state='A').exists()

    def get_rubric_ac_by_ac(self, ac=None):
        try:
            return self.select_related('ac').filter(
                ac=ac,
                ac__state=1,
                ac__auth_state='A',
                state=1,
                auth_state='A'
            )
        except:
            return None


