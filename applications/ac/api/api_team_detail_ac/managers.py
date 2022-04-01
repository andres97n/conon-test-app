

from django.db import models


class TeamDetailAcManager(models.Manager):

    def get_team_ac_active_queryset(self):
        return self.select_related('owner', 'team_ac').filter(active=True, auth_state='A')

    def get_team_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('owner', 'team_ac').filter(id=pk, active=True, auth_state='A')
        except:
            return None

    def get_team_detail_ac_list(self):
        return self.get_team_ac_active_queryset().order_by('-created_at')

    def exists_user_in_team_ac(self, team=None, user=None):
        return self.select_related('owner', 'team_ac').filter(
            team_ac=team,
            team_ac__ac__state=1,
            team_ac__auth_state='A',
            owner=user,
            owner__is_active=True,
            owner__auth_state='A',
            active=True,
            auth_state='A'
        ).exists()

    def get_team_ac_students_count(self, pk=None):
        queryset = self.get_team_ac_active_object_queryset(pk=pk)
        if queryset is not None:
            return queryset.count()
        else:
            return 0

    def exists_team_detail_ac(self, pk=None):
        return self.filter(id=pk, active=True, auth_state='A').exists()
