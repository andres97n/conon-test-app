
from django.db import models


class ProblemResolutionStepEightAbpManager(models.Manager):

    def get_problem_resolution_step_eight_list(self):
        return self.select_related('team_abp').filter(auth_state='A').order_by('-created_at')
