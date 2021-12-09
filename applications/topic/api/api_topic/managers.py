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

    def get_students_by_topic_id(self, pk=None, active=None):
        try:
            if active is not None:
                return self.filter(id=pk, active=True, auth_state='A').values(
                    'students',
                    'students__person__identification',
                    'students__person__name',
                    'students__person__last_name',
                    'students__person__age',
                    'students__person__user'
                )
            else:
                return self.filter(id=pk, auth_state='A').values(
                    'students',
                    'students__person__identification',
                    'students__person__name',
                    'students__person__last_name',
                    'students__person__age',
                    'students__person__user'
                )
        except:
            return None

    def get_topics_by_owner(self, user=None):
        try:
            return self.select_related('owner').filter(
                owner_id=user, active=True, auth_state='A'
            )
        except:
            return None
