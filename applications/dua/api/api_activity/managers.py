from django.db import models


class ActivityManager(models.Manager):

    def get_activity_list(self):
        return self.select_related('topic').filter(auth_state='A').order_by('created_at')

    def get_activity_by_id(self, pk=None):
        activity = None
        try:
            activity = self.select_related('topic').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            pass
        return activity

    def activity_exists(self, pk=None):
        result = None
        try:
            result = self.filter(id=pk, auth_state='A')
        except None:
            pass

        if result is not None:
            return True
        return False
