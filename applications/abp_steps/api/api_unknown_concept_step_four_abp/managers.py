
from django.db import models


class UnknownConceptStepFourAbpManager(models.Manager):

    def get_unknown_concept_abp_list(self):
        return self.select_related('team_abp').filter(auth_state='A').order_by('-created_at')

    def unknown_concept_exists(self, concept=None):
        return self.filter(id=concept, active=True, auth_state='A')

    def get_unknown_concepts_by_team(self, team=None):
        try:
            return self.select_related('team_abp').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

