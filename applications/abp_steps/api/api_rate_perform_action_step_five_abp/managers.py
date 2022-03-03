
from django.db import models


class RatePerformActionStepFiveAbpManager(models.Manager):

    def get_rate_perform_action_abp_list(self):
        return self.select_related('perform_action_step_five_abp', 'user').\
            filter(auth_state='A').order_by('-created_at')

    def get_rate_perform_action_list_by_action(self, action=None, active=None):
        try:
            return self.select_related('perform_action_step_five_abp', 'user').filter(
                perform_action_step_five_abp=action,
                perform_action_step_five_abp__active=active,
                perform_action_step_five_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
