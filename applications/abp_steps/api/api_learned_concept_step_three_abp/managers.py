from django.db import models


class LearnedConceptStepThreeAbpManager(models.Manager):

    def get_learned_concept_list(self):
        return self.select_related('team_abp').filter(auth_state='A').order_by('-created_at')

    def learned_concept_exists(self, pk=None):
        return self.filter(id=pk, active=True, auth_state='A').exists()
