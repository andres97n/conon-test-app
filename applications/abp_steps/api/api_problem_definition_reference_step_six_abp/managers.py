
from django.db import models


class ProblemDefinitionReferenceStepFixAbpManager(models.Manager):

    def get_problem_definition_references_list(self):
        return self.select_related('team_abp', 'user').filter(auth_state='A')\
            .order_by('-created_at')

    def get_definition_reference_by_team(self, team=None, reference_active=None):
        try:
            return self.select_related('team_abp', 'user').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__abp__auth_state='A',
                active=reference_active,
                auth_state='A'
            )
        except:
            return None
