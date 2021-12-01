from django.db import models


class ClassroomManager(models.Manager):

    def get_classroom_list(self):
        return self.filter(auth_state='A').order_by('state', 'name')

    def get_classroom_active_list(self):
        return self.filter(state=1, auth_state='A').order_by('state', 'name')

    def get_classroom_by_id(self, pk=None):
        try:
            return self.filter(id=pk, state=1, auth_state='A').first()
        except:
            return None

    def is_active(self, pk=None):
        classroom = None
        try:
            classroom = self.select_related('school_period').filter(
                id=pk,
                auth_state='A',
                school_period__state=1
            ).first()
        except:
            pass
        if classroom is None:
            return False
        else:
            return True

    def get_many_classrooms(self, classrooms=None):
        try:
            self.filter(auth_state='A').values('asignatureclassroom__asignature__knowledge_area_id ')
            if classrooms is not None:
                return list(self.in_bulk(classrooms).values())
            return None
        except:
            return None

    def get_short_classroom(self):
        return self.filter(state=1, auth_state='A').values(
            'id',
            'name',
            'curse_level'
        ).order_by('name')

    def get_students_by_classroom_id(self, pk=None):
        try:
            return self.filter(id=pk, state=1, auth_state='A').values(
                'students',
                'students__person__identification',
                'students__person__name',
                'students__person__last_name',
                'students__person__age'
            )
        except:
            return None
