from django.db import models


class TopicManager(models.Manager):

    def get_topic_list(self):
        return self.select_related('owner').filter(auth_state='A').order_by('title')

    def get_topic_by_id(self, pk=None):
        topic = None
        try:
            topic = self.select_related('owner').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            pass
        return topic

    def topic_exists(self, pk=None):
        result = None
        try:
            result = self.filter(id=pk, active=True, auth_state='A').first()
        except None:
            pass
        return result
