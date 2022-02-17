from django.db import models


class TeamDetailAbpManager(models.Manager):

    def get_team_detail_abp_by_id(self, pk=None):
        try:
            return self.select_related('team_abp', 'user').\
                filter(auth_state='A', active=True).get(id=pk)
        except:
            return None

    def get_team_detail_abp_list(self):
        return self.select_related('team_abp', 'user').\
            filter(auth_state='A', active=True).order_by('-created_at')

    def is_user_moderator(self, user=None, team=None):
        return self.filter(
            team_abp=team, user=user, is_moderator=True, auth_state='A'
        ).exists()

    def exists_team_detail_abp(self, pk=None):
        return self.filter(id=pk, auth_state='A').exists()

    # Get active opinions for the current user
    def get_opinions_step_one_by_user(self, team=None):
        try:
            return self.select_related('user', 'team_abp').filter(
                id=team,
                opinionsteponeabp__active=True,
                opinionsteponeabp__auth_state='A',
                auth_state='A'
            ).values(
                'opinionsteponeabp',
                'opinionsteponeabp__opinion',
                'opinionsteponeabp__active',
                'opinionsteponeabp__created_at'
            )
        except:
            return None

    # Get active opinions for the team
    def get_opinions_step_one_exclude_user(self, team=None, user=None):
        try:
            return self.select_related('user', 'team_abp').filter(
                team_abp=team,
                opinionsteponeabp__active=True,
                opinionsteponeabp__auth_state='A',
                auth_state='A'
            ).exclude(user=user).values(
                'opinionsteponeabp',
                'opinionsteponeabp__opinion',
                'opinionsteponeabp__active',
                'opinionsteponeabp__created_at'
            )
        except:
            return None

