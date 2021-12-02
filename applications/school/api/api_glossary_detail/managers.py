from django.db import models


class GlossaryDetailManager(models.Manager):

    # TODO: Cambiar los nombres de los métodos por el nombre correcto

    def get_glosary_detail_list(self):
        return self.select_related('glossary'). \
            filter(auth_state='A').order_by('-created_at', '-updated_at')

    def get_glosary_detail_by_id(self, pk=None):
        result = None
        try:
            result = self.select_related('glossary'). \
                filter(id=pk, auth_state='A').first()
        except:
            pass
        return result

    def title_exists(self, pk=None, title=None):
        result = None
        try:
            result = self.select_related('glossary').filter(
                glosary_id=pk,
                title=title,
                auth_state='A'
            )
        except:
            pass

        if result is None:
            return False

        return True

    def get_glossary_detail_by_glossary(self, pk=None):
        try:
            return self.select_related('glossary').filter(
                glossary_id=pk, state=1, auth_state='A'
            )
        except:
            return None

    def get_many_glossaries_detail(self, terms=None):
        try:
            if terms is not None:
                return list(self.in_bulk(terms).values())
            return None
        except:
            return None
