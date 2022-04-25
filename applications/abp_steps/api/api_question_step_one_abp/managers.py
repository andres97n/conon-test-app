from django.db import models


class QuestionStepOneAbpManager(models.Manager):

    def get_question_abp_list(self):
        return self.select_related('team_abp').filter(auth_state='A').order_by('-created_at')

    def get_question_abp_by_pk(self, pk=None):
        try:
            return self.select_related('team_abp').filter(auth_state='A').get(id=pk)
        except:
            return None

    def exists_question_abp(self, pk=None):
        return self.filter(id=pk, auth_state='A').exists()

    def get_questions_count_by_team_abp(self, team=None):
        try:
            return self.select_related('team_abp').\
                filter(team_abp=team, active=True, auth_state='A').count()
        except:
            return None

    def get_questions_abp_by_team(self, team=None):
        try:
            return self.select_related('team_abp').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    def get_answers_by_team(self, team=None):
        try:
            return self.select_related('team_abp').filter(
                team_abp=team,
                team_abp__state=1,
                team_abp__auth_state='A',
                active=True,
                auth_state='A'
            ).values(
                'id',
                'answersteponeabp',
                'answersteponeabp__user',
                'answersteponeabp__teacher_answer',
                'answersteponeabp__active',
                'answersteponeabp__created_at'
            )
        except:
            return None

