from django.db import models


class ConversationDetailManager(models.Manager):

    def __str__(self):
        return self.detail

    def get_conversation_detail_list(self):
        return self.select_related('conversation', 'owner').filter(auth_state='A').order_by('-send_date')

    def get_conversation_detail_by_pk(self, pk=None):
        conversation_detail = None
        try:
            conversation_detail = self.select_related('conversation', 'owner'). \
                filter(id=pk, auth_state='A').first()
        except None:
            pass
        return conversation_detail

    def get_conversation_detail_by_conversation_pk(self, pk=None):
        conversation = None
        try:
            conversation = self.select_related('conversation', 'owner'). \
                filter(auth_state='A', conversation=pk). \
                order_by('-send_date')
        except None:
            pass
        return conversation

    def is_owner_in_conversation(self, conversation_id=None, pk=None):
        user_1, user_2 = None, None
        try:
            user_1 = self.filter(
                conversation_id=conversation_id,
                conversation__first_user_id=pk,
                conversation__blocked=False,
                conversation__auth_state='A'
            )
        except None:
            pass

        try:
            user_2 = self.filter(
                conversation_id=conversation_id,
                conversation__second_user_id=pk,
                conversation__blocked=False,
                conversation__auth_state='A'
            )
        except None:
            pass

        if (user_1 is not None) or (user_2 is not None):
            return True
        else:
            return False


