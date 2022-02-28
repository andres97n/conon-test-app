
from django.db import models


class LearnedConceptReferenceStepThreeAbpManager(models.Manager):

    def get_learned_concept_reference_list(self):
        return self.select_related('learned_concept_step_three_abp', 'user').filter(
            auth_state='A'
        ).order_by('-created_at')

    def get_learned_concept_reference_by_concept(self, concept=None, active=None):
        try:
            return self.select_related('learned_concept_step_three_abp', 'user').filter(
                learned_concept_step_three_abp=concept,
                learned_concept_step_three_abp__active=active,
                learned_concept_step_three_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    def get_learned_concepts_references_by_concept(self, concept=None):
        try:
            return self.select_related('learned_concept_step_three_abp', 'user').filter(
                learned_concept_step_three_abp=concept,
                learned_concept_step_three_abp__active=True,
                learned_concept_step_three_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

