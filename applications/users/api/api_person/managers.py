from django.db import models


class PersonManager(models.Manager):

    # Get Person data to a Student
    def is_deleted(self, pk=None):
        person = None
        try:
            person = self.filter(id=pk, auth_state='A').first()
        except:
            pass
        return person

    def get_person_list(self):
        return self.filter(auth_state='A').order_by('last_name')

    def get_person_detail_data(self, pk=None):
        person = None
        try:
            person = self.filter(id=pk, auth_state='A').first()
        except:
            pass

        return person
