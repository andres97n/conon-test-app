from django.db import models


class SchoolPeriodManager(models.Manager):

    def get_period_list(self):
        return self.filter(auth_state='A').order_by('name')

    def get_period_by_pk(self, pk=None):
        period = None
        try:
            period = self.filter(id=pk, auth_state='A')
        except:
            pass

        return period

    def is_period_active(self, pk=None):
        period = None
        try:
            period = self.filter(id=pk, state=1, auth_state='A').first()
        except:
            pass
        if period:
            return True
        else:
            return False
