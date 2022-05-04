
from django.db import models


class DescribeUnderstandingOrganizerAcManager(models.Manager):

    def get_describe_understanding_organizer_ac_active_queryset(self):
        return self.select_related('team_detail_ac', 'member_ac').filter(
            team_detail_ac__active=True,
            team_detail_ac__auth_state='A',
            member_ac__active=True,
            member_ac__auth_state='A',
            active=True,
            auth_state='A'
        )

    def get_describe_understanding_organizer_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('team_detail_ac', 'member_ac').filter(
                team_detail_ac__active=True,
                team_detail_ac__auth_state='A',
                member_ac__active=True,
                member_ac__auth_state='A',
                active=True,
                auth_state='A'
            ).get(id=pk)
        except:
            return None

    def get_describe_understanding_organizer_ac_list(self):
        return self.get_describe_understanding_organizer_ac_active_queryset().order_by('-created_at')
