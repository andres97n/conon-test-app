
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

    def team_ac_by_ac(self, ac=None, user=None):
        try:
            return self.select_related('ac').filter(
                ac=ac,
                ac__state=1,
                ac__auth_state='A',
                teamdetailac__owner=user,
                teamdetailac__active=True,
                teamdetailac__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    def get_team_ac_by_ac(self, ac=None):
        try:
            return self.select_related('ac').filter(
                ac=ac,
                ac__state=1,
                ac__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    def is_team_ac_finished(self, team=None):
        try:
            return self.select_related('team_ac').filter(
                id=team,
                team_state=0,
                active=True,
                auth_state='A',
            )
        except:
            return None

