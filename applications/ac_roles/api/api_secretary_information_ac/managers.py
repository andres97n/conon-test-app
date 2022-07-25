
from django.db import models


class SecretaryInformationAcManager(models.Manager):

    def get_secretary_information_ac_active_queryset(self):
        return self.select_related('team_ac').filter(
            team_ac__active=True,
            team_ac__auth_state='A',
            active=True,
            auth_state='A'
        )

    def get_secretary_information_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('team_ac').filter(
                team_ac__active=True,
                team_ac__auth_state='A',
                active=True,
                auth_state='A'
            ).get(id=pk)
        except:
            return None

    def get_secretary_information_ac_list(self):
        return self.get_secretary_information_ac_active_queryset().order_by('-created_at')

    def get_secretary_information_by_team(self, team_ac=None):
        try:
            return self.select_related('team_ac').filter(
                team_ac=team_ac,
                team_ac__active=True,
                team_ac__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
