
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_state = models.CharField(max_length=1, default='A')

    class Meta:
        abstract = True


class Person(BaseModel):
    # GENDERS
    FEMININE = '0'
    MASCULINE = '1'
    OTHER = '2'

    GENDER_CHOICES = [
        (FEMININE, 'Feminine'),
        (MASCULINE, 'Masculine'),
        (OTHER, 'Other'),
    ]

    identification = models.CharField(
        max_length=30,
        unique=True,
        blank=False
    )
    name = models.CharField(
        max_length=50,
        blank=False
    )
    surname = models.CharField(
        max_length=80,
        blank=False
    )
    gender = models.CharField(
        max_length=15,
        blank=True,
        choices=GENDER_CHOICES
    )
    age = models.CharField(
        max_length=2,
        blank=True
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    class Meta:
        db_table = 'person'
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        return f'{self.identification} - {self.full_name()}'

    def full_name(self):
        return f'{self.name} {self.surname}'


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    # USERS
    ADMINISTRATOR = '0'
    TEACHER = '1'
    STUDENT = '2'

    USERS_CHOICES = [
        (ADMINISTRATOR, 'Administrator'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]

    username = models.CharField(
        max_length=30,
        unique=True
    )
    email = models.EmailField(
        null=True,
        blank=True,

    )
    type = models.CharField(
        max_length=1,
        choices=USERS_CHOICES,
        blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=True
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        'email'
    ]

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email
