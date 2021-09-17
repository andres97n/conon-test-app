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

    def user_list(self):
        return self.select_related('person').filter(is_active=True).values(
            'id',
            'username',
            'person__name',
            'person__last_name',
            'email',
            'type',
            'is_superuser'
        ).order_by('username')

    def get_user_data(self):
        return self.select_related('person').filter(auth_state='A', is_active=True).order_by('username')

    def get_user_detail_data(self, pk=None):
        user = None
        try:
            user = self.select_related('person').filter(
                id=pk,
                is_active=True,
                auth_state='A'
            ).first()
        except:
            pass

        return user
