from django.db import models


class ConversationDetailManager(models.Manager):

    def get_conversation_detail_list(self):
        return self.select_related('conversation', 'owner').\
            filter(auth_state='A').order_by('-created_at')

    def get_conversation_detail_by_pk(self, pk=None):
        try:
            return self.select_related('conversation', 'owner'). \
                filter(blocked=False, auth_state='A').get(id=pk)
        except None:
            return None

    def get_active_conversation_detail(self):
        return self.select_related('first_user', 'second_user').filter(
            blocked=False,
            auth_state='A'
        )

    def get_conversation_detail_by_conversation_pk(self, pk=None):
        try:
            return self.select_related('conversation', 'owner').filter(
                conversation=pk,
                conversation__blocked=False,
                conversation__auth_state='A',
                blocked=False,
                auth_state='A'
            ).order_by('-created_at')
        except None:
            return None

    def not_view_messages_owner(self, user=None):
        try:
            return self.select_related('owner').filter(
                owner=user,
                owner__is_active=True,
                owner__auth_state='A',
                blocked=False,
                state=0,
                auth_state='A'
            ).count()
        except:
            return None
