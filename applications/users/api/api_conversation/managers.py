from django.db import models


class ConversationManager(models.Manager):

    def get_conversation_list(self):
        return self.select_related('first_user', 'second_user').filter(blocked=False, auth_state='A').order_by('-created_at')

    def get_conversation_by_pk(self, pk=None):
        conversation = None
        try:
            conversation = self.select_related('first_user', 'second_user').filter(
                id=pk,
                blocked=False,
                auth_state='A'
            ).first()
        except None:
            pass
        return conversation

    # Optional
    def get_conversation_detail_by_pk(self, pk=None):
        conversation = None
        try:
            conversation = self.filter(conversation_detail__owner__conversation=pk).order_by(
                '-conversation_detail__send_date')
        except None:
            pass
        return conversation

    def conversation_exists(self, pk=None):
        result = None,
        try:
            result = self.filter(id=pk, blocked=False, auth_state='A').first()
        except None:
            pass

        if result is not None:
            return True

        return False

    def are_users_in_conversation(self, pk_1=None, pk_2=None):
        conversation_1, conversation_2 = None, None
        try:
            conversation_1 = self.filter(
                first_user_id=pk_1,
                second_user_id=pk_2,
                blocked=False,
                auth_state='A'
            ).first()
        except None:
            pass
        try:
            conversation_2 = self.filter(
                first_user_id=pk_2,
                second_user_id=pk_1,
                blocked=False,
                auth_state='A'
            ).first()
        except None:
            pass

        if (conversation_1 is not None) or (conversation_2 is not None):
            return False

        return True
