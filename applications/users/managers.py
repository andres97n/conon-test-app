from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username, email, password, type, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            type=type,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, username, email, password=None, type=None, **extra_fields):
        return self._create_user(username, email, password, type, False, False, True, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, '0', True, True, True, **extra_fields)

    def get_email(self):
        return self.email

    def user_data(self):
        return self.select_related('person').filter(is_active=True, auth_state='A').values(
            'id',
            'username',
            'person__name',
            'person__last_name',
            'email',
            'type',
            'is_superuser',
            'created_at'
        ).order_by('username')

    def get_user_data(self):
        return self.select_related('person').\
            filter(auth_state='A', is_active=True).order_by('username')

    def get_user_detail_data(self, pk=None):
        try:
            return self.select_related('person').filter(
                id=pk,
                is_active=True,
                auth_state='A'
            ).first()
        except None:
            return None

    def user_exists(self, pk=None):
        return self.filter(id=pk, is_active=True, auth_state='A').exists()

    def type_user_exists(self, pk=None, prototype=None):
        return self.filter(id=pk, type=prototype, is_active=True, auth_state='A').exists()

    def validate_user_type(self, pk=None):
        users = None
        is_admin, is_teacher, is_student, is_valid = False, False, False, True

        try:
            users = self.select_related('person').filter(
                person_id=pk,
                is_active=True,
                auth_state='A'
            ).values('type')
        except None:
            pass

        if users:
            for user in users:
                if user['type'] == 0:
                    is_admin = True
                elif user['type'] == 1:
                    is_teacher = True
                elif user['type'] == 2:
                    is_student = True

            # The student cannot be an admin or a teacher
            if is_student and type == 0:
                is_valid = False
            if is_student and type == 1:
                is_valid = False

            # The admin or the teacher cannot be a student
            if is_admin and type == 2:
                is_valid = False
            if is_teacher and type == 2:
                is_valid = False

        return is_valid

    def get_many_users(self, users=None):
        result = None
        try:
            if users is not None:
                result = list(self.in_bulk(users).values())
        except:
            pass
        return result

    def get_name_by_user_id(self, pk=None):
        try:
            return self.select_related('person').filter(id=pk, auth_state='A').values(
                'person__name',
                'person__last_name'
            ).first()
        except:
            return None

    def exists_username(self, username=None):
        return self.filter(username=username, is_active=True, auth_state='A').exists()

    def get_email_by_user(self, user=None):
        try:
            return self.filter(
                is_active=True,
                auth_state='A'
            ).get(id=user)
        except:
            return None

    def get_user_by_username(self, username=None):
        try:
            return self.filter(username=username, is_active=True, auth_state='A').first()
        except:
            return None


