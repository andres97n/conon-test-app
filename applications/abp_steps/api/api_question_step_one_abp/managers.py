from django.db import models


class QuestionStepOneAbpManager(models.Manager):

    def get_question_abp_list(self):
        return self.select_related('team_abp').filter(auth_state='A').order_by('-created_at')

    def get_question_abp_by_pk(self, pk=None):
        try:
            return self.select_related('team_abp').filter(id=pk, auth_state='A')
        except:
            return None

    def exists_question_abp(self, pk=None):
        return self.filter(id=pk, auth_state='A').exists()


