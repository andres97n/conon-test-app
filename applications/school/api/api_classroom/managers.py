from django.db import models


class ClassroomManager(models.Manager):

    def get_classroom_list(self):
        return self.filter(auth_state='A').order_by('state', 'name')

    def get_classroom_active_list(self):
        return self.filter(state=1, auth_state='A').order_by('state', 'name')

    def get_classroom_by_id(self, pk=None):
        try:
            return self.filter(state=1, auth_state='A').get(id=pk)
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
            self.filter(auth_state='A').values(
                'asignatureclassroom__asignature__knowledge_area_id'
            )
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
                'students__person__age',
                'students__person__user',
            )
        except:
            return None

    def get_classrooms_by_teacher(self, pk=None):
        try:
            return self.select_related('school_period').filter(
                asignatureclassroom__teacher_id=pk,
                state=1,
                auth_state='A'
            ).distinct('id')
        except:
            return None

    def exists_classroom(self, classroom=None):
        return self.filter(id=classroom, state=1, auth_state='A').exists()

    def get_classroom_by_student_and_period(self, period=None, student=None):
        try:
            return self.select_related('school_period').filter(
                school_period=period,
                school_period__state=1,
                school_period__auth_state='A',
                state=1,
                auth_state='A',
                students=student,
            ).first()
        except:
            return None

    def get_classroom_by_student_assigned(self, student=None):
        try:
            return self.select_related('school_period').filter(
                school_period__state=1,
                school_period__auth_state='A',
                students=student,
                state=1,
                auth_state='A'
            )
        except:
            return None

    def exists_student_in_classroom(self, student=None):
        return self.select_related('school_period').filter(
            school_period__state=1,
            school_period__auth_state='A',
            students=student,
            state=1,
            auth_state='A'
        ).exists()
