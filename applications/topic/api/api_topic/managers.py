from django.db import models


class TopicManager(models.Manager):

    def get_topic_list(self):
        return self.select_related('owner').filter(auth_state='A').\
            order_by('-created_at', 'active')

    def get_topic_by_id(self, pk=None):
        try:
            return self.select_related('owner').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            return None

    def topic_exists(self, pk=None):
        result = None
        try:
            result = self.filter(id=pk, active=True, auth_state='A').first()
        except None:
            pass
        return result

    def get_topics_by_type(self, type=None):
        try:
            self.filter()
            return self.select_related('owner', 'owner__person').filter(
                type=type, auth_state='A'
            ).order_by('-created_at', 'active')
        except:
            return None

    def get_many_topics(self, topics=None):
        try:
            if topics is not None:
                return list(self.in_bulk(topics).values())
            else:
                return None
        except:
            return None
