from django.db import models


class TeamAbpManager(models.Manager):

    def get_team_abp_by_id(self, pk=None):
        try:
            return self.select_related('abp').filter(auth_state='A', state=1).get(id=pk)
        except:
            return None

    def get_team_abp_list(self):
        return self.select_related('abp'). \
            filter(auth_state='A').order_by('-created_at')

    def team_abp_exists(self, pk=None):
        try:
            result = self.filter(auth_state='A', state=1).get(id=pk)
            if result:
                return True
            else:
                return False
        except:
            return False

    def get_ids_team_detail_abp_by_team_abp(self, pk=None):
        try:
            return self.filter(
                id=pk,
                state=1,
                auth_state='A',
                teamdetailabp__active=True,
                teamdetailabp__auth_state='A'
            ).values(
                'teamdetailabp__user_id',
            )
        except:
            return None

    def get_detail_by_team_abp(self, pk=None):
        try:
            return self.filter(
                id=pk,
                state=1,
                auth_state='A',
                teamdetailabp__auth_state='A'
            ).values(
                'id',
                'step',
                'teamdetailabp__id',
                'teamdetailabp__user_id',
                'teamdetailabp__is_moderator',
                'teamdetailabp__active'
            )
        except:
            return None

    def get_team_abp_list_by_abp(self, abp_id):
        try:
            return self.select_related('abp').filter(abp_id=abp_id, state=1, auth_state='A')
        except:
            return None

    def get_count_of_users_in_team_abp(self, pk=None):
        try:
            return self.filter(
                id=pk,
                state=1,
                auth_state='A',
                teamdetailabp__active=True,
                teamdetailabp__auth_state='A'
            ).values(
                'teamdetailabp__user_id'
            ).count()
        except:
            return None

    def exists_moderator_in_team_abp(self, pk=None):
        return self.filter(
                id=pk, auth_state='A', state=1, teamdetailabp__is_moderator=True
        ).exists()

    def exists_user_in_team_abp(self, pk=None, user_id=None):
        try:
            if self.filter(
                id=pk, auth_state='A', state=1, teamdetailabp__user_id=user_id
            ).exists():
                return True
            else:
                return False
        except:
            return False

    def get_team_by_user_and_abp(self, abp=None, user=None):
        try:
            return self.select_related('abp').\
                filter(abp_id=abp, teamdetailabp__user_id=user, auth_state='A').values(
                'id',
            ).first()
        except:
            return None

    def get_ids_team_detail_abp_by_team_abp_exclude_active(self, pk=None):
        try:
            return self.filter(
                id=pk,
                state=1,
                teamdetailabp__auth_state='A',
                auth_state='A',
            ).values(
                'teamdetailabp__user',
            )
        except:
            return None

    def get_questions_and_answers_step_one_by_team(self, pk=None):
        try:
            return self.filter(
                id=pk,
                questionsteponeabp__active=True,
                questionsteponeabp__answersteponeabp__active=True,
                state=1,
                auth_state='A'
            ).values(
                'questionsteponeabp',
                'questionsteponeabp__moderator_question',
                'questionsteponeabp__answersteponeabp',
                'questionsteponeabp__answersteponeabp__user_id',
                'questionsteponeabp__answersteponeabp__teacher_answer'
            )
        except:
            return None
