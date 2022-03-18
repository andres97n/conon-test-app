from django.db import models


class TopicStudentEvaluationManager(models.Manager):

    def get_topic_student_evaluation_list(self):
        return self.select_related('user', 'topic').filter(auth_state='A').\
            order_by('-created_at')

    def is_topic_student_evaluation_type(self, pk=None, prototype=None):
        return self.select_related('user', 'topic').filter(
            id=pk,
            topic__active=True,
            topic__auth_state='A',
            user__is_active=True,
            user__auth_state='A',
            type=prototype,
            active=True,
            auth_state='A'
        ).exists()
