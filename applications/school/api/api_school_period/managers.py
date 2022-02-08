from django.db import models


class SchoolPeriodManager(models.Manager):

    def mapper(self):
        return dict(
            name=self.name,
            init_date=self.init_date,
            end_date=self.end_date,
            school_end_date=self.school_end_date,
            state=self.state.__str__(),
            observations=self.observations
        )

    def get_period_list(self):
        return self.filter(auth_state='A').order_by('name')

    def get_period_active_list(self):
        return self.filter(state=1, auth_state='A').order_by('name')

    def get_period_by_pk(self, pk=None):
        period = None
        try:
            period = self.filter(id=pk, auth_state='A').first()
        except None:
            pass

        return period

    def is_period_active(self, pk=None):
        period = None
        try:
            period = self.filter(id=pk, state=1, auth_state='A').first()
        except None:
            pass
        if period:
            return True
        else:
            return False

    def is_name_exists(self, name=None):
        return self.filter(name=name, auth_state='A').exists()

    def get_many_school_periods(self, periods=None):
        try:
            if periods is not None:
                return list(self.in_bulk(periods).values())
            return None
        except:
            return None

    def get_school_periods_active(self):
        return self.filter(state=1, auth_state='A').values(
            'id', 'name'
        )

    def get_period_active(self):
        return self.filter(state=1, auth_state='A').first()
