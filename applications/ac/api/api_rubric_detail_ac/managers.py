
from django.db import models


class RubricDetailAcManager(models.Manager):

    def get_rubric_detail_ac_active_queryset(self):
        return self.select_related('rubric_ac').filter(active=True, auth_state='A')

    def get_rubric_detail_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('rubric_ac').filter(id=pk, active=True, auth_state='A')
        except:
            return None

    def get_rubric_detail_ac_list(self):
        return self.get_rubric_detail_ac_active_queryset().order_by('-created_at')

    def exists_rubric_detail_ac(self, pk=None):
        return self.filter(id=pk, active=True, auth_state='A')

    def get_rubric_detail_ac_by_rubric_ac(self, rubric=None):
        try:
            return self.select_related('rubric_ac').filter(
                rubric_ac=rubric,
                rubric_ac__state=1,
                rubric_ac__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

