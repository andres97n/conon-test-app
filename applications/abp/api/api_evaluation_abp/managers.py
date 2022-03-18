from django.db import models


class EvaluationAbpManager(models.Manager):

    def get_evaluation_abp_by_id(self, pk=None):
        try:
            return self.select_related('abp', 'team_detail_abp').filter(
                abp__state=1,
                abp__auth_state='A',
                team_detail_abp__active=True,
                team_detail_abp__auth_state='A',
                state=1,
                auth_state='A',
            ).get(id=pk)
        except:
            return None

    def get_evaluation_abp_list(self):
        return self.select_related('abp', 'team_detail_abp').\
            filter(auth_state='A').order_by('-created_at')

    def evaluation_abp_exists(self, pk=None):
        return self.filter(id=pk, state=1, auth_state='A').exists()

    def get_evaluation_abp_by_abp_and_team_detail(self, abp=None, team_detail=None):
        try:
            return self.select_related('abp', 'team_detail_abp').filter(
                abp=abp,
                abp__state=1,
                abp__auth_state='A',
                team_detail_abp=team_detail,
                team_detail_abp__active=True,
                team_detail_abp__auth_state='A',
                state=1,
                auth_state='A',
            ).first()
        except:
            return None
        