from django.db import models


class TeamDetailAbpManager(models.Manager):

    def get_team_detail_abp_by_id(self, pk=None):
        try:
            return self.select_related('team_abp', 'user'). \
                filter(auth_state='A', active=True).get(id=pk)
        except:
            return None

    def get_team_detail_abp_list(self):
        return self.select_related('team_abp', 'user'). \
            filter(auth_state='A', active=True).order_by('-created_at')

    def is_user_moderator(self, user=None, team=None):
        return self.filter(
            team_abp=team, user=user, is_moderator=True, auth_state='A'
        ).exists()

    def exists_team_detail_abp(self, pk=None):
        return self.filter(id=pk, auth_state='A').exists()

    # Get active opinions for the current user
    def get_opinions_step_one_by_user(self, team_detail=None):
        try:
            return self.select_related('user', 'team_abp').filter(
                id=team_detail,
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

    # Get active student ideas for the team
    def get_team_student_idea_step_two_exclude_user(self, team=None, user=None):
        try:
            return self.select_related('team_abp', 'user').filter(
                team_abp=team,
                studentideasteptwoabp__active=True,
                studentideasteptwoabp__auth_state='A',
                auth_state='A'
            ).exclude(user=user).values(
                'studentideasteptwoabp',
                'studentideasteptwoabp__student_idea',
                'studentideasteptwoabp__active',
                'studentideasteptwoabp__created_at'
            )
        except:
            return None

    def get_opinion_ids_step_one_abp_by_team(self, team=None):
        try:
            self.select_related('team_abp').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__abp__auth_state='A',
                active=True,
                auth_state='A',
            ).values(
                'opinionsteponeabp'
            )
        except:
            return None

    def get_team_detail_count_by_team(self, team=None):
        try:
            self.select_related('team_abp').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__abp__auth_state='A',
                active=True,
                auth_state='A',
            ).aggregate(
                students_count=models.Count('id')
            )
        except:
            return None

    # Agrupar por opinion
    def get_unpopular_interactions_step_one_abp_by_team(self, team=None):
        try:
            return self.select_related('team_abp').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__abp__auth_state='A',
                active=True,
                auth_state='A',
                opinionsteponeabp__interactionsteponeabp__opinion_interaction=1
            ).annotate(
                unpopular_interactions=models.Count(
                    'opinionsteponeabp__interactionsteponeabp'
                )
            ).order_by('unpopular_interactions')
        except:
            return None

    # Get Team Details By Team And Exclude User
    def get_team_detail_list_by_team_exclude_user(self, team=None, user=None):
        try:
            return self.select_related('team_abp', 'user').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__abp__auth_state='A',
                user__is_active=True,
                user__auth_state='A',
                active=True,
                auth_state='A',
            ).exclude(user=user)
        except:
            return None

    def get_team_detail_by_team(self, team=None):
        try:
            return self.select_related('team_abp', 'user').filter(
                team_abp=team,
                team_abp__abp__auth_state='A',
                auth_state='A'
            )
        except:
            return None
