from django.db import models


# TODO: Mejorar las consultas con las relaciones sobre todo con la
#   relación topic


class CommentManager(models.Manager):

    def get_comment_list(self):
        return self.select_related('topic', 'owner').filter(
            state=True,
            auth_state='A'
        ).order_by('-created_at')

    def get_comment_by_id(self, pk=None):
        comment = None
        try:
            comment = self.select_related('topic', 'owner').filter(
                id=pk,
                state=True,
                auth_state='A'
            ).get()
        except None:
            pass
        return comment

    def title_exists(self, pk=None, title=None):
        comment = None
        try:
            comment = self.select_related('topic').filter(
                topic_id=pk, title=title, state=True, auth_state='A'
            )
        except None:
            pass

        if comment.exists():
            return True
        return False

    def comment_exists(self, pk=None):
        result = None
        try:
            result = self.filter(id=pk, state=True, auth_state='A')
        except None:
            pass

        if result.exists():
            return True
        return False
