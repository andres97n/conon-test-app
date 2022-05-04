
from django.db import models


class PerformanceDescriptionSpokesmanAcManager(models.Manager):

    def get_performance_description_spokesman_ac_active_queryset(self):
        return self.select_related('team_detail_ac').filter(
            team_detail_ac__active=True,
            team_detail_ac__auth_state='A',
            active=True,
            auth_state='A'
        )

    def get_performance_description_spokesman_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('team_detail_ac').filter(
                team_detail_ac__active=True,
                team_detail_ac__auth_state='A',
                active=True,
                auth_state='A'
            ).get(id=pk)
        except:
            return None

    def get_performance_description_spokesman_ac_list(self):
        return self.get_performance_description_spokesman_ac_active_queryset().order_by('-created_at')



