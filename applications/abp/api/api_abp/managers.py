from django.db import models


class AbpManager(models.Manager):

    def get_abp_by_id(self, pk=None):
        abp = None
        try:
            abp = self.select_related('topic').filter(auth_state='A', state=1).get(id=pk)
        except:
            pass
        return abp

    def get_abp_list(self):
        return self.select_related('topic').filter(auth_state='A', state=1).order_by('-created_at')

    def abp_exists(self, pk=None):
        try:
            return self.filter(state=1, auth_state='A').get(id=pk)
        except:
            return None

    def get_abp_by_topic(self, topic=None):
        try:
            return self.select_related('topic').filter(auth_state='A').get(topic=topic)
        except:
            return None
