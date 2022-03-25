from django.db import models


class QuestionManager(models.Manager):

    def get_question_list(self):
        return self.select_related('activity').filter(auth_state='A').order_by('created_at')

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

    def question_exists(self, pk=None):
        return self.filter(
            id=pk,
            active=True,
            auth_state='A'
        ).exists()

    def get_questions_by_activity(self, activity=None):
        try:
            return self.select_related('activity').filter(
                activity=activity,
                activity__state=1,
                activity__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

