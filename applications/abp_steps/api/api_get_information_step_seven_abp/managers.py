
from django.db import models


class GetInformationStepSevenAbpManager(models.Manager):

    def get_information_step_seven_list(self):
        return self.select_related('team_abp').filter(auth_state='A').order_by('-created_at')

    def get_information_model_by_team(self, team=None):
        try:
            return self.select_related('team_abp').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

