
from django.db import models


class RateStudentIdeaStepTwoAbpManager(models.Manager):

    def get_rate_student_idea_abp_list(self):
        return self.select_related('user', 'student_idea_step_two_abp').\
            filter(auth_state='A').\
            order_by('-created_at')

    def get_rate_student_idea_abp_by_pk(self, pk=None):
        try:
            return self.select_related('user', 'student_idea_step_two_abp').\
                filter(auth_state='A').get(id=pk)
        except:
            return None

    def get_rate_student_ideas_by_idea(self, student_idea=None):
        try:
            return self.select_related('student_idea_step_two_abp', 'user').filter(
                student_idea_step_two_abp=student_idea,
                student_idea_step_two_abp__active=True,
                student_idea_step_two_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    def get_count(self):
        return self.filter(auth_state='A').count()

    def get_any_rate_student_ideas_by_idea(self, student_idea=None):
        try:
            return self.select_related('student_idea_step_two_abp', 'user').filter(
                student_idea_step_two_abp=student_idea,
                student_idea_step_two_abp__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
