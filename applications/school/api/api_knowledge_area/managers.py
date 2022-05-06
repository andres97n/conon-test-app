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
        try:
            return self.select_related(
                'coordinator',
                'sub_coordinator'
            ).filter(auth_state='A').get(id=pk)
        except:
            return None

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

    def get_teachers_by_area_id(self, pk=None):
        teachers = None
        try:
            # teachers = self.filter(id=pk, auth_state='A').values_list('teachers', flat=True)
            teachers = self.filter(id=pk, auth_state='A').values(
                'teachers',
                'teachers__person__identification',
                'teachers__person__name',
                'teachers__person__last_name',
                'teachers__title'
            )
        except:
            pass
        return teachers

    def get_teachers_count(self, pk=None):
        try:
            return self.filter(
                pk=pk, auth_state='A', teachers__isnull=True
            ).count()
        except:
            return 1

    def get_many_areas(self, areas=None):
        try:
            if areas is not None:
                return list(self.in_bulk(areas).values())
        except:
            return None

    def get_teachers_area(self):
        try:
            return self.filter(auth_state='A').values(
                'id',
                'teachers__id',
                'teachers__person__identification',
                'teachers__person__name',
                'teachers__person__last_name',
                'teachers__title'
            )
        except:
            return None

    def is_type_exits(self, prototype=None):
        return self.filter(type=prototype, auth_state='A').exists()

    def get_teachers_ids_by_area(self, area=None):
        try:
            return self.filter(id=area, auth_state='A').values(
                'teachers__id'
            )
        except:
            return None

