
from django.db import models


class StudentEvaluationAcManager(models.Manager):
    def get_student_evaluation_ac_active_queryset(self):
        return self.select_related('rubric_ac', 'team_detail_ac').filter(state=1, auth_state='A')

    def get_student_evaluation_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('rubric_ac', 'team_detail_ac').filter(
                id=pk, state=1, auth_state='A'
            )
        except:
            return None

    def get_student_evaluation_ac_list(self):
        return self.get_student_evaluation_ac_active_queryset().order_by('-created_at')

    def exists_student_evaluation_ac(self, pk=None):
        return self.filter(id=pk, state=1, auth_state='A').exists()

