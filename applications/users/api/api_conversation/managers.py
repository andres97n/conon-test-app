from django.db import models


class ConversationManager(models.Manager):

    def get_conversation_list(self):
        return self.select_related('first_user', 'second_user').\
            filter(blocked=False, auth_state='A').order_by('-created_at')

    def get_conversation_by_pk(self, pk=None):
        try:
            return self.select_related('first_user', 'second_user').filter(
                blocked=False,
                auth_state='A'
            ).get(id=pk)
        except None:
            return None

    def get_active_conversation(self):
        return self.select_related('first_user', 'second_user').filter(
            blocked=False,
            auth_state='A'
        )

    def conversation_exists(self, pk=None):
        return self.filter(id=pk, blocked=False, auth_state='A').exists()

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

    def user_exists_like_first_in_conversation(self, user=None):
        try:
            return self.select_related('first_user').filter(
                first_user=user,
                first_user__is_active=True,
                first_user__auth_state='A',
                blocked=False,
                auth_state='A'
            )
        except:
            return None

    def user_exists_like_second_in_conversation(self, user=None):
        try:
            return self.select_related('second_user').filter(
                second_user=user,
                second_user__is_active=True,
                second_user__auth_state='A',
                blocked=False,
                auth_state='A'
            )
        except:
            return None

    def is_owner_in_conversation(self, user=None):
        user_first = self.user_exists_like_first_in_conversation(user=user)
        user_second = self.user_exists_like_second_in_conversation(user=user)
        if user_first or user_second:
            if user_first.exists():
                return True
            elif user_second.exists():
                return True
        return False

    def get_conversations_by_user_id(self, user=None):
        try:
            first_user = self.select_related('first_user', 'second_user').filter(
                first_user=user,
                first_user__is_active=True,
                first_user__auth_state='A',
                second_user__is_active=True,
                second_user__auth_state='A',
                state=1,
                auth_state='A'
            )
            second_user = self.select_related('first_user', 'second_user').filter(
                second_user=user,
                second_user__is_active=True,
                second_user__auth_state='A',
                first_user__is_active=True,
                first_user__auth_state='A',
                state=1,
                auth_state='A'
            )
            return {
                'first_user': first_user,
                'second_user': second_user
            }
        except:
            return None
