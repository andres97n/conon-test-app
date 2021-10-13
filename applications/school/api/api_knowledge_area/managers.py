from django.db import models


class KnowledgeAreaManager(models.Manager):

    def get_sub_coordinator(self):
        return f'{self.sub_coordinator.person.name} {self.sub_coordinator.person.last_name}'

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
        except None:
            pass

        return area

    def is_active(self, pk=None):
        knowledge_area = None
        try:
            knowledge_area = self.filter(id=pk, auth_state='A').first()
        except None:
            pass
        if knowledge_area is None:
            return False

        return True

    def is_name_exists(self, name=None):
        knowledge_area = None
        try:
            knowledge_area = self.filter(name=name, auth_state='A').first()
        except None:
            pass
        if knowledge_area is None:
            return False
        return True
