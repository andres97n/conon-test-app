from django.db import models


class CommentManager(models.Manager):

    def get_comment_list(self):
        return self.select_related('topic', 'owner').filter(auth_state='A').\
            order_by('-created_at')

    def get_comment_by_id(self, pk=None):
        try:
            return self.select_related('topic', 'owner').filter(
                auth_state='A'
            ).get(id=pk)
        except:
            return None

    def title_exists(self, pk=None, title=None):
        return self.select_related('topic').filter(
            topic_id=pk, title=title, state=True, auth_state='A'
        ).exists()

    def comment_exists(self, pk=None):
        return self.filter(id=pk, state=True, auth_state='A').exists()

    def get_comment_by_topic(self, topic=None):
        try:
            return self.select_related('topic', 'owner').filter(
                topic=topic,
                auth_state='A'
            ).order_by('-created_at', '-state')
        except:
            return None
