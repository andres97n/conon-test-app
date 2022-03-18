from django.db import models


class EvaluationDetailAbpManager(models.Manager):

    def get_evaluation_detail_abp_by_id(self, pk=None):
        try:
            return self.select_related('evaluation_abp').filter(auth_state='A', active=True).get(id=pk)
        except:
            return None

    def get_evaluation_detail_abp_list(self):
        return self.select_related('evaluation_abp').\
            filter(auth_state='A').order_by('-created_at')

    def get_evaluation_details_by_evaluations(self, evaluation=None):
        try:
            return self.select_related('evaluation_abp').filter(
                evaluation_abp=evaluation,
                evaluation_abp__state=1,
                evaluation_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
