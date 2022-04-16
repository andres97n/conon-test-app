
from django.db import models


class StudentEvaluationAcManager(models.Manager):
    def get_student_evaluation_ac_active_queryset(self):
        return self.select_related('rubric_ac', 'team_detail_ac').filter(auth_state='A')

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

    def get_evaluation_ac_by_rubric_and_team_detail(self, rubric=None, team_detail=None):
        try:
            return self.select_related('rubric_ac', 'team_detail_ac').filter(
                rubric_ac=rubric,
                rubric_ac__state=1,
                rubric_ac__auth_state='A',
                team_detail_ac=team_detail,
                team_detail_ac__active=True,
                team_detail_ac__auth_state='A',
                state=1,
                auth_state='A',
            )
        except:
            return None
