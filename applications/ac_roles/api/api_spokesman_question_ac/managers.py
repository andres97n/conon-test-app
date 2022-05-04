
from django.db import models


class SpokesmanQuestionAcManager(models.Manager):
    def get_spokesman_question_ac_active_queryset(self):
        return self.select_related('team_detail_ac').filter(
            team_detail_ac__active=True,
            team_detail_ac__auth_state='A',
            active=True,
            auth_state='A'
        )

    def get_spokesman_question_ac_active_object_queryset(self, pk=None):
        try:
            return self.select_related('team_detail_ac').filter(
                team_detail_ac__active=True,
                team_detail_ac__auth_state='A',
                active=True,
                auth_state='A'
            ).get(id=pk)
        except:
            return None

    def get_spokesman_question_ac_list(self):
        return self.get_spokesman_question_ac_active_queryset().order_by('-created_at')

    def exists_spokesman_question_ac(self, pk=None):
        return self.filter(id=pk, auth_state='A').exists()

    def get_questions_by_team_detail(self, team_detail=None):
        try:
            return self.select_related('team_detail_ac').filter(
                team_detail_ac=team_detail,
                team_detail_ac__active=True,
                team_detail_ac__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None
