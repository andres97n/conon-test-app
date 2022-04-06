from django.db import models


class DuaManager(models.Manager):

    def get_dua_list(self):
        return self.select_related('topic').filter(auth_state='A').order_by('created_at')

    def get_dua_by_id(self, pk=None):
        dua = None
        try:
            dua = self.select_related('topic').filter(
                id=pk,
                auth_state='A'
            ).first()
        except None:
            pass
        return dua

    def get_dua_by_topic(self, pk=None):
        try:
            print(pk)
            return self.select_related('topic').filter(
                state=1, auth_state='A'
            ).get(topic_id=pk)
        except:
            return None

    def exists_dua(self, pk=None):
        try:
            # return self.filter(id=pk, state=1, auth_state='A').exists()
            result = self.filter(id=pk, state=1, auth_state='A')
            if result:
                return True
            else:
                return False
        except:
            return None

    def get_students_by_dua(self, pk=None):
        try:
            return self.select_related('topic').filter(id=pk, state=1, auth_state='A').values(
                'topic__students',
                'topic__students__person_id',
            )
        except:
            return None
