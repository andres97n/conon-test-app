
from django.db import models


class TeacherAnswerAcManager(models.Manager):

    def get_teacher_answer_ac_active_queryset(self):
        return self.select_related('teacher', 'spokesman_question_ac').filter(
            teacher__auth_state='A',
            spokesman_question_ac__active=True,
            spokesman_question_ac__auth_state='A',
            active=True,
            auth_state='A'
        )

    def get_teacher_answer_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('teacher', 'spokesman_question_ac').filter(
                teacher__auth_state='A',
                spokesman_question_ac__active=True,
                spokesman_question_ac__auth_state='A',
                active=True,
                auth_state='A'
            ).get(id=pk)
        except:
            return None

    def get_teacher_answer_ac_list(self):
        return self.get_teacher_answer_ac_active_queryset().order_by('-created_at')

    def exists_teacher_answer(self, pk=None):
        return self.filter(id=pk, auth_state='A').exists()

    def get_answer_by_question(self, question=None):
        try:
            return self.select_related('teacher', 'spokesman_question_ac').filter(
                spokesman_question_ac=question,
                spokesman_question_ac__active=True,
                spokesman_question_ac__auth_state='A',
                teacher__auth_state='A',
                active=True,
                auth_state='A'
            ).first()
        except:
            return None
