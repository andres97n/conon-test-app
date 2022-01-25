from django.db import models


class EvaluationDetailAbpManager(models.Manager):

    def get_evaluation_detail_abp_by_id(self, pk=None):
        try:
            return self.select_related('evaluation_abp').filter(auth_state='A', active=True).get(id=pk)
        except:
            return None

    def get_evaluation_detail_abp_list(self):
        return self.select_related('evaluation_abp').\
            filter(auth_state='A', active=True).order_by('--created_at')

