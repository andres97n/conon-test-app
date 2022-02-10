from django.db import models


class RubricAbpManager(models.Manager):

    def get_rubric_abp_by_id(self, pk=None):
        try:
            return self.select_related('abp').filter(auth_state='A', state=1).get(id=pk)
        except:
            return None

    def get_rubric_abp_list(self):
        return self.select_related('abp').\
            filter(auth_state='A', state=1).order_by('-created_at')

    def rubric_exists(self, pk=None):
        try:
            result = self.filter(auth_state='A', state=1).get(id=pk)
            if result:
                return True
            else:
                return False
        except:
            return False

    def get_rubric_detail_by_pk(self, pk=None):
        try:
            return self.filter(
                id=pk, auth_state='A'
            ).values(
                'id',
                'abp_final_value',
                'rubricdetailabp',
                'rubricdetailabp__title_detail',
                'rubricdetailabp__description_detail',
                'rubricdetailabp__grade_percentage',
                'rubricdetailabp__rating_value',
                'rubricdetailabp__active'
            )
        except:
            return None

    def get_rubric_detail_by_abp(self, abp=None):
        try:
            return self.filter(
                abp=abp, auth_state='A'
            ).values(
                'id',
                'abp_final_value',
                'rubricdetailabp',
                'rubricdetailabp__title_detail',
                'rubricdetailabp__description_detail',
                'rubricdetailabp__grade_percentage',
                'rubricdetailabp__rating_value',
                'rubricdetailabp__active'
            )
        except:
            return None

    def get_rubric_abp_by_abp(self, abp=None):
        return self.select_related('abp').\
            filter(abp=abp, auth_state='A')
