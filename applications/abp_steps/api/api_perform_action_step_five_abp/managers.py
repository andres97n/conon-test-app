
from django.db import models


class PerformActionStepFiveAbpManager(models.Manager):

    def get_perform_action_abp_list(self):
        return self.select_related('team_detail_abp').filter(auth_state='A').order_by('-created_at')

    def perform_action_exists(self, perform=None):
        return self.filter(id=perform, active=True, auth_state='A').exists()

    def get_student_perform_action_by_team_detail(self, team_detail=None):
        try:
            return self.select_related('team_detail_abp').filter(
                team_detail_abp=team_detail,
                team_detail_abp__active=True,
                team_detail_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    # Get Actions And Rates By Team
    def get_actions_by_team_exclude_user(self, team=None, user=None):
        try:
            return self.select_related(
                'team_detail_abp',
                'team_detail_abp__user',
                'team_detail_abp__team_abp'
            ). filter(
                team_detail_abp__team_abp=team,
                team_detail_abp__team_abp__state=1,
                team_detail_abp__team_abp__auth_state='A',
                team_detail_abp__active=True,
                team_detail_abp__auth_state='A',
                active=True,
                auth_state='A'
            ).exclude(team_detail_abp__user=user)
        except:
            return None

    def get_student_actions_by_team(self, team=None):
        try:
            return self.select_related(
                'team_detail_abp',
                'team_detail_abp__team_abp',
                'team_detail_abp__user'
            ).filter(
                team_detail_abp__team_abp=team,
                team_detail_abp__team_abp__state=1,
                team_detail_abp__team_abp__auth_state='A',
                team_detail_abp__active=True,
                team_detail_abp__auth_state='A',
                active=True,
                auth_state='A'
            ).order_by('team_detail_abp')
        except:
            return None

