from django.db import models


class ActivityStudentManager(models.Manager):

    def get_activity_student_list(self):
        self.select_related('activity', 'owner').filter(auth_state='A').order_by('created_at')

    def get_activity_student_by_id(self, pk=None):
        data = None
        try:
            data = self.select_related('activity', 'owner').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            pass
        return data

    def activity_student_exists(self, pk=None):
        result = None
        try:
            result = self.filter(id=pk, auth_state='A')
        except None:
            pass

        if result is not None:
            return True
        return False
