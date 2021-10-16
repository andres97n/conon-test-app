from django.db import models


class QuestionManager(models.Manager):

    def get_question_list(self):
        return self.select_related('activity').filter(active=True, auth_state='A').order_by('created_at')

    def get_question_by_id(self, pk=None):
        question = None
        try:
            question = self.select_related('activity').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            pass
        return question

    def question_exists(self):
        result = None
        try:
            result = self.filter(id=pk, auth_state='A')
        except None:
            pass

        if result is not None:
            return True
        return False
