
from django.db import models


class TeamAcManager(models.Manager):

    def get_team_ac_active_queryset(self):
        return self.select_related('ac').filter(active=True, auth_state='A')

    def get_team_ac_active_object_queryset(self, pk=None):
        return self.select_related('ac').filter(id=pk, active=True, auth_state='A')

    def get_team_ac_list(self):
        return self.get_team_ac_active_queryset().order_by('-created_at')

    def exists_team_ac(self, pk=None):
        return self.get_team_ac_active_object_queryset(pk=pk).exists()


