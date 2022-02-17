from django.db import models


class InteractionStepOneAbpManager(models.Manager):

    def get_interaction_abp_list(self):
        return self.select_related('opinion_step_one_abp', 'user').filter(auth_state='A').\
            order_by('-created_at')

    def get_interaction_abp_by_pk(self, pk=None):
        try:
            return self.select_related('opinion_step_one_abp', 'user').\
                filter(auth_state='A').get(id=pk)
        except:
            return None

    def get_many_interactions(self, interactions=None):
        try:
            return list(self.in_bulk(interactions).values())
        except:
            return None
