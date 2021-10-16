from django.db import models


class AnswerManager(models.Manager):

    def get_answer_list(self):
        return self.select_related('activity_student', 'question').filter(auth_state='A'). \
            order_by('created_at')

    def get_answer_by_id(self, pk=None):
        answer = None
        try:
            answer = self.select_related('activity_student', 'question').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            pass
        return answer
