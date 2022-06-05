from django.db import models


class GlossaryManager(models.Manager):

    # TODO: Cambiar los nombres de los métodos por el nombre correcto

    def get_glosary_list(self):
        return self.select_related('asignature_classroom'). \
            filter(auth_state='A').order_by('created_at')

    def get_glosary_by_id(self, pk=None):
        try:
            return self.select_related('asignature_classroom'). \
                filter(id=pk, auth_state='A').first()
        except None:
            return None

    def glosary_exists(self, pk=None):
        return self.filter(id=pk, state=1, auth_state='A').exists()

    def get_glossary_state(self, pk=None):
        glossary = None
        try:
            glossary = self.filter(state=1, auth_state='A').get(id=pk)
        except:
            pass
        if glossary is None:
            return False

        return True

    def get_glossary_by_classroom(self, classroom=None):
        try:
            return self.select_related('classroom').filter(
                classroom=classroom,
                classroom__state=1,
                classroom__auth_state='A',
                state=1,
                auth_state='A'
            )
        except:
            return None

