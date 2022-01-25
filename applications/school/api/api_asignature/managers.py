from django.db import models


class AsignatureManager(models.Manager):

    def is_active(self, pk=None):
        asignature = None
        try:
            asignature = self.filter(id=pk, auth_state='A').first()
        except None:
            pass
        if asignature is None:
            return False

        return True

    def get_asignature_list(self):
        return self.select_related('knowledge_area').\
            filter(auth_state='A').order_by('name')

    def get_asignature_list_active(self):
        return self.select_related('knowledge_area').\
            filter(auth_state='A', state=1).order_by('name')

    def get_asignature_by_id(self, pk=None):
        try:
            return self.select_related('knowledge_area').\
                filter(auth_state='A', state=1).get(id=pk)
        except:
            return None

    def get_many_asignatures(self, asignatures=None):
        try:
            if asignatures is not None:
                return list(self.in_bulk(asignatures).values())
            return None
        except:
            return None

    def get_asignature_detail_by_pk(self, pk=None):
        asignatures = None
        try:
            asignatures = self.filter(id=pk, state=1, auth_state='A').values(
                'classrooms__asignatureclassroom__teacher_id'
                # 'asignatureclassroom_id',
                # 'asignatureclassroom__classroom_id',
                # 'asignatureclassroom__teacher_id',
            )
        except :
            pass

        return asignatures
