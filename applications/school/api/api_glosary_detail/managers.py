from django.db import models


class GlosaryDetailManager(models.Manager):

    def get_glosary_detail_list(self):
        return self.select_related('glosary'). \
            filter(auth_state='A').order_by('-created_at', '-updated_at')

    def get_glosary_detail_by_id(self, pk=None):
        result = None
        try:
            result = self.select_related('glosary'). \
                filter(id=pk, auth_state='A').first()
        except None:
            pass
        return result

    def title_exists(self, pk=None, title=None):
        result = None
        try:
            result = self.select_related('glosary').filter(
                glosary_id=pk,
                title=title,
                auth_state='A'
            )
        except None:
            pass
        if result.exists():
            return True

        return False
