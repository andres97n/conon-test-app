from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def new_user(self, username, email, password, type, is_staff, is_superuser, is_active, **extra_fields):
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

    def create_user(self, username, email, password=None, **extra_fields):
        return self.new_user(username, email, password, None, False, False, True, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self.new_user(username, email, password, '0', True, True, True, **extra_fields)


