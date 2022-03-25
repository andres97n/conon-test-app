from django.db import models


class ActivityManager(models.Manager):

    def get_activity_list(self):
        return self.select_related('dua').filter(auth_state='A').order_by('created_at')

    def get_activity_by_id(self, pk=None):
        activity = None
        try:
            activity = self.select_related('dua').filter(
                id=pk,
                state=1,
                auth_state='A'
            ).first()
        except None:
            pass
        return activity

    def activity_exists(self, pk=None):
        return self.filter(id=pk, state=1, auth_state='A').exists()

    def get_questions_by_activity(self, pk=None):
        try:
            return self.filter(id=pk, state=1, auth_state='A').values(
                'question',
                'question__title',
                'question__answers',
                'question__value'
            )
        except:
            return None

    def get_activity_by_dua(self, dua=None):
        try:
            return self.select_related('dua').filter(
                dua=dua,
                dua__state=1,
                dua__auth_state='A',
                state=1,
                auth_state='A'
            )
        except:
            return None
