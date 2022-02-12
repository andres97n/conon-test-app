from django.db import models


class OpinionStepOneAbpManager(models.Manager):

    def get_opinion_abp_list(self):
        return self.select_related('team_detail_abp').filter(auth_state='A').order_by('-created_at')

    def get_opinion_abp_by_pk(self, pk=None):
        try:
            return self.select_related('team_detail_abp').filter(auth_state='A').get(id=pk)
        except:
            return None

    def exists_opinion_abp(self, pk=None):
        return self.filter(id=pk, auth_state='A').exists()

    def get_interactions_step_one_abp_by_opinion(self, opinion=None):
        try:
            return self.filter(
                id=opinion, auth_state='A'
            ).values(
                'interactionsteponeabp',
                'interactionsteponeabp__user',
                'interactionsteponeabp__opinion_interaction',
                'interactionsteponeabp__active',
                'interactionsteponeabp__created_at'
            )
        except:
            return None
