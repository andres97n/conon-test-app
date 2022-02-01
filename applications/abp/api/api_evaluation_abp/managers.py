from django.db import models


class EvaluationAbpManager(models.Manager):

    def get_evaluation_abp_by_id(self, pk=None):
        try:
            return self.select_related('abp', 'user').filter(auth_state='A', state=1).get(id=pk)
        except:
            return None

    def get_evaluation_abp_list(self):
        return self.select_related('abp', 'user').\
            filter(auth_state='A', state=1).order_by('-created_at')

    def evaluation_abp_exists(self, pk=None):
        try:
            result = self.filter(auth_state='A', state=1).get(id=pk)
            if result:
                return True
            else:
                return False
        except:
            return False
