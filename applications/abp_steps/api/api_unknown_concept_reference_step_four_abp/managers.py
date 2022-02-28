
from django.db import models


class UnknownConceptReferenceStepFourAbpManager(models.Manager):

    def get_unknown_concept_reference_list(self):
        return self.select_related('unknown_concept_step_four_abp', 'user').filter(
            auth_state='A'
        ).order_by('-created_at')

    def get_unknown_concept_reference_by_concept(self, concept=None, active=None):
        try:
            return self.select_related('unknown_concept_step_four_abp', 'user').filter(
                unknown_concept_step_four_abp=concept,
                unknown_concept_step_four_abp__active=active,
                unknown_concept_step_four_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
