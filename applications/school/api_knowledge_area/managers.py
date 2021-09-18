from django.db import models


class KnowledgeAreaManager(models.Manager):

    def get_area_list(self):
        return self.select_related(
            'coordinator',
            'sub_coordinator'
        ).filter(auth_state='A').order_by('name')

    def get_are_by_id(self, pk=None):
        area = None
        try:
            area = self.select_related(
                'coordinator',
                'sub_coordinator'
            ).filter(id=pk, auth_state='A').first()
        except:
            pass

        return area
