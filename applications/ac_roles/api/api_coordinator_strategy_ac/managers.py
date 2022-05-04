
from django.db import models


class CoordinatorStrategyAcManager(models.Manager):

    def get_coordinator_strategy_ac_active_queryset(self):
        return self.select_related('team_detail_ac').filter(
            team_detail_ac__active=True,
            team_detail_ac__auth_state='A',
            active=True,
            auth_state='A'
        )

    def get_coordinator_strategy_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('team_detail_ac').filter(
                id=pk,
                team_detail_ac__active=True,
                team_detail_ac__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    def get_coordinator_strategy_ac_list(self):
        return self.get_coordinator_strategy_ac_active_queryset().order_by('-created_at')

