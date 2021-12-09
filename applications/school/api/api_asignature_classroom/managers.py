from django.db import models


class AsignatureClassroomManager(models.Manager):

    def get_asignature_classroom_list(self):
        return self.select_related(
            'classroom',
            'asignature',
            'teacher'
        ).filter(auth_state='A').order_by('classroom__name')

    def get_asignature_classroom_by_id(self, pk=None):
        asignature_classroom = None
        try:
            asignature_classroom = self.select_related(
                'classroom',
                'asignature',
                'teacher'
            ).filter(id=pk, auth_state='A').first()
        except None:
            pass
        return asignature_classroom

    def asignature_classroom_exists(self, pk=None):
        result = None
        try:
            result = self.filter(id=pk, auth_state='A')
        except None:
            pass

        if result is None:
            return False

        return True

    def get_asignature_classroom_active(self):
        return self.select_related('classroom', 'asignature', 'teacher'). \
            filter(state=1, auth_state='A').values(
            'id',
            'classroom_id',
            'asignature_id',
            'teacher_id'
        )

    def get_asignature_classroom_by_asignature_short(self, pk=None):
        try:
            return self.select_related('classroom', 'teacher'). \
                filter(asignature_id=pk, state=1, auth_state='A').values(
                'id',
                'classroom_id',
                'teacher_id',
            )
        except:
            return None

    def get_asignature_classroom_by_asignature(self, pk=None):
        try:
            return self.select_related('classroom', 'teacher'). \
                filter(asignature_id=pk, state=1, auth_state='A').order_by('created_at')
        except:
            return None

    def get_asignature_classroom_by_classroom_and_teacher(self, classroom_id=None, teacher_id=None):
        try:
            return self.select_related('classroom', 'teacher').filter(
                classroom_id=classroom_id, teacher_id=teacher_id, state=1, auth_state='A'
            )
        except:
            return None
