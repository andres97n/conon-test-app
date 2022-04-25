from django.db import models


class TeacherManager(models.Manager):

    def mapper(self):
        return dict(
            id=self.id,
            name=self.person.name,
            last_name=self.person.last_name,
            identification=self.person.identification,
            phone=self.person.phone,
            title=self.title,
            objective=self.objective
        )

    # Get Person data of the Teacher
    def get_teacher_by_id(self, pk=None):
        teacher = None
        try:
            teacher = self.select_related('person').filter(id=pk, auth_state='A').first()
        except:
            pass
        return teacher

    # Get Active Teacher List
    def get_teacher_list(self):
        teachers = self.select_related('person').filter(auth_state='A').order_by('person__last_name')
        return teachers

    # Return if the Teacher is active
    def is_active(self, pk=None):
        teacher = None
        try:
            teacher = self.filter(id=pk, auth_state='A').first()
        except:
            pass
        if teacher is None:
            return False

        return True

    def get_user(self, pk=None):
        result = None
        try:
            result = self.filter(person__user__type=1, auth_state='A'). \
                values_list(
                'person__user__id', 'person__user__username', 'person__user__email',
            ).get(id=pk)
        except:
            pass
        return result

    def get_many_teachers(self, teachers=None):
        result = None
        try:
            if teachers is not None:
                result = list(self.in_bulk(teachers).values())
        except:
            pass
        return result

    def get_coordinators_data(self):
        teachers = self.select_related('person').filter(auth_state='A'). \
            values(
            'id',
            'person__name',
            'person__last_name'
        )
        return teachers

    def get_teachers_short_data(self):
        return self.select_related('person').filter(auth_state='A'). \
            values(
            'id',
            'person__identification',
            'person__name',
            'person__last_name',
            'title'
        ).order_by('person__last_name')

    def get_user_id_by_teacher(self, pk=None):
        try:
            return self.select_related('person').filter(auth_state='A').values(
                'person__user'
            ).get(id=pk)
        except:
            return None

    def get_teacher_by_user(self, pk=None):
        try:
            return self.select_related('person').filter(person__user=pk).values(
                'id'
            ).get()
        except:
            return None

    def get_teacher_object_by_user(self, user=None):
        try:
            return self.select_related('person').filter(
                person__user=user,
                person__auth_state='A',
                person__user__is_active=True,
                person__user__auth_state='A',
                auth_state='A'
            ).first()
        except:
            return None

    def get_teacher_list_exclude_owner(self, owner=None):
        try:
            return self.select_related('person').filter(
                person__auth_state='A',
                auth_state='A'
            ).order_by('person__last_name').exclude(id=owner).values(
                'id',
                'person__identification',
                'person__name',
                'person__last_name',
                'title',
                'person__user'
            )
        except:
            return None
