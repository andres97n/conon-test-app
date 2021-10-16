from django.db import models


class ReplyManager(models.Manager):

    def get_reply_list(self):
        return self.select_related('comment', 'owner').filter(auth_state='A'). \
            order_by('-created_at')

    def get_reply_by_id(self, pk=None):
        reply = None
        try:
            reply = self.select_related('comment', 'owner').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            pass
        return reply

