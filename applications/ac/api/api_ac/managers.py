
from django.db import models


class AcManager(models.Manager):

    def get_ac_active_queryset(self):
        return self.select_related('topic').filter(state=1, auth_state='A')

    def get_ac_active_object_queryset(self, pk=None):
        return self.select_related('topic').filter(id=pk, state=1, auth_state='A')

    def get_ac_list(self):
        return self.get_ac_active_queryset().order_by('-created_at')

    def exists_ac_methodology(self, pk=None):
        return self.filter(id=pk, state=1, auth_state='A').exists()

    def get_ac_by_topic(self, topic=None):
        try:
            return self.select_related('topic').filter(auth_state='A').get(topic=topic)
        except:
            return None

