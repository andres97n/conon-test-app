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
        user = None
        try:
            user = self.select_related('person').filter(
                id=pk,
                is_active=True,
                auth_state='A'
            ).first()
        except None:
            pass
        return user

    def user_exists(self, pk=None):
        result = None
        try:
            result = self.filter(id=pk, is_active=True, auth_state='A').first()
        except None:
            pass

        if result is not None:
            return True

        return False

    def student_user_exists(self, pk=None):
        try:
            if self.filter(id=pk, type=2, is_active=True, auth_state='A').exists():
                return True
            else:
                return False
        except:
            return False

    def validate_user_type(self, pk=None, type=None):
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

            # The admin or the teacher cannot be an student
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
