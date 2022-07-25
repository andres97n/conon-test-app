from django.db import models


class ActivityStudentManager(models.Manager):

    def get_activity_student_list(self):
        return self.select_related('activity', 'owner').\
            filter(auth_state='A').order_by('-created_at')

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
        return self.filter(id=pk, active=True, auth_state='A')

    def activity_student_by_activity_and_owner(self, activity=None, owner=None):
        try:
            return self.select_related('activity', 'owner').filter(
                activity=activity,
                activity__state=1,
                activity__auth_state='A',
                owner=owner,
                owner__is_active=True,
                owner__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    def is_activity_student_exists_by_activity_and_owner(self, activity=None, owner=None):
        return self.filter(
            activity=activity,
            activity__state=1,
            activity__auth_state='A',
            owner=owner,
            owner__is_active=True,
            owner__auth_state='A',
            active=True,
            auth_state='A'
        ).exists()

    def get_activity_student_by_dua(self, dua=None, owner=None):
        try:
            return self.select_related('activity', 'owner', 'activity__dua').filter(
                owner=owner,
                activity__dua=dua,
                owner__is_active=True,
                owner__auth_state='A',
                activity__dua__auth_state='A',
                activity__auth_state='A',
                auth_state='A'
            )
        except:
            return None
