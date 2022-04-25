from django.db import models


class RubricDetailAbpManager(models.Manager):

    def get_rubric_detail_abp_by_id(self, pk=None):
        try:
            return self.select_related('rubric_abp').filter(auth_state='A', active=True).get(id=pk)
        except:
            return None

    def get_rubric_detail_abp_list(self):
        return self.select_related('rubric_abp').\
            filter(auth_state='A', active=True).order_by('-created_at')

    def get_rubric_abp_detail_by_rubric(self, rubric=None):
        try:
            return self.select_related('rubric_abp').filter(
                rubric_abp=rubric,
                rubric_abp__state=1,
                rubric_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
