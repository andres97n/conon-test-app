from django.db import models


class AnswerStepOneAbpManager(models.Manager):

    def get_answer_abp_list(self):
        return self.select_related('question_step_one_abp', 'user').filter(auth_state='A').\
            order_by('-created_at')

    def get_answer_abp_by_pk(self, pk=None):
        try:
            return self.select_related('question_step_one_abp', 'user').\
                filter(auth_state='A').get(id=pk)
        except:
            return None

    def get_answers_step_one_by_question(self, question=None):
        try:
            return self.filter(
                question_step_one_abp=question,
                active=True,
                auth_state='A'
            )
        except:
            return None

    def get_answer_step_one_by_team(self, team=None):
        try:
            return self.select_related(
                'question_step_one_abp', 'user', 'question_step_one_abp__team_abp'
            ).filter(
                question_step_one_abp__team_abp=team,
                question_step_one_abp__team_abp__state=1,
                question_step_one_abp__team_abp__auth_state='A',
                question_step_one_abp__active=True,
                question_step_one_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
