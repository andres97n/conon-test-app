from django.db import models


class StudentIdeaStepTwoAbpManager(models.Manager):

    def get_student_idea_abp_list(self):
        return self.select_related('team_detail_abp').filter(auth_state='A').\
            order_by('-created_at')

    def get_student_idea_abp_by_pk(self, pk=None):
        try:
            return self.select_related('team_detail_abp').\
                filter(auth_state='A').get(id=pk)
        except:
            return None

    def exists_student_idea(self, pk=None):
        return self.filter(id=pk, active=True, auth_state='A').exists()

    # Get student ideas by user
    def get_student_ideas_abp_by_team_detail(self, team_detail=None):
        try:
            return self.select_related('team_detail_abp').filter(
                team_detail_abp=team_detail,
                team_detail_abp__active=True,
                team_detail_abp__auth_state='A',
                active=True,
                auth_state='A'
            ).order_by('created_at')
        except:
            return None
