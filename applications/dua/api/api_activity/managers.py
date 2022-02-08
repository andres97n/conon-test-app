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
        result = None
        try:
            result = self.filter(id=pk, state=1, auth_state='A')
        except None:
            pass

        if result is not None:
            return True
        return False

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

