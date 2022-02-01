from django.db import models


class TeamDetailAbpManager(models.Manager):

    def get_team_detail_abp_by_id(self, pk=None):
        try:
            return self.select_related('team_abp', 'user').filter(auth_state='A', active=True).get(id=pk)
        except:
            return None

    def get_team_detail_abp_list(self):
        return self.select_related('team_abp', 'user').\
            filter(auth_state='A', active=True).order_by('-created_at')
