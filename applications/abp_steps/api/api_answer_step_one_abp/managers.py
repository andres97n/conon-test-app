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
