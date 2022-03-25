from django.db import models


class AnswerManager(models.Manager):

    def get_answer_list(self):
        return self.select_related('activity_student', 'question').filter(auth_state='A'). \
            order_by('-created_at')

    def get_answer_by_id(self, pk=None):
        try:
            return self.select_related('activity_student', 'question').filter(
                active=True,
                auth_state='A'
            ).get(id=pk)
        except None:
            return None

    def get_answers_by_activity_student(self, activity_student):
        try:
            return self.select_related('activity_student', 'question').filter(
                activity_student=activity_student,
                activity_student__active=True,
                activity_student__auth_state='A',
                question__active=True,
                question__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
