
from django.db import models


class StudentEvaluationDetailAcManager(models.Manager):
    def get_student_evaluation_detail_ac_active_queryset(self):
        return self.select_related('rubric_detail_ac', 'student_evaluation_ac').filter(auth_state='A')

    def get_student_evaluation_detail_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('rubric_detail_ac', 'student_evaluation_ac').filter(
                id=pk, auth_state='A'
            )
        except:
            return None

    def get_student_evaluation_detail_ac_list(self):
        return self.get_student_evaluation_detail_ac_active_queryset().order_by('-created_at')

    def exists_student_activity_detail_ac(self, pk=None):
        return self.filter(id=pk, auth_state='A').exists()

    def get_evaluation_details_by_evaluation_ac(self, evaluation=None):
        try:
            return self.select_related('student_evaluation_ac', 'rubric_detail_ac').filter(
                student_evaluation_ac=evaluation,
                student_evaluation_ac__state=1,
                student_evaluation_ac__auth_state='A',
                rubric_detail_ac__active=True,
                rubric_detail_ac__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
