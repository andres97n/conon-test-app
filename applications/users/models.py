from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

from applications.base.models import BaseModel
from applications.users.managers import UserManager
from applications.users.api.api_student.managers import StudentManager
from applications.users.api.api_teacher.managers import TeacherManager
from applications.users.api.api_person.managers import PersonManager


# TODO: Cambiar el tipo de campo a JSON de
#   expectations y observations


class Person(BaseModel):

    # GENDERS
    class GenderChoices(models.IntegerChoices):
        FEMININE = 0
        MASCULINE = 1
        OTHER = 2

    class IdentificationChoices(models.IntegerChoices):
        CI = 0
        OTHER = 1

    identification_type = models.PositiveIntegerField(
        choices=IdentificationChoices.choices,
        default=0,
        null=False,
        blank=False,
    )

    identification = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )
    name = models.CharField(
        max_length=80,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    gender = models.PositiveSmallIntegerField(
        choices=GenderChoices.choices,
        null=False,
        blank=False,
    )
    age = models.PositiveIntegerField(
        null=False,
        blank=False
    )
    phone = models.CharField(
        max_length=20,
        null=False,
        blank=False,
    )

    objects = PersonManager()

    class Meta:
        db_table = 'person'
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        return f'{self.identification} - {self.full_name()}'

    def full_name(self):
        return f'{self.name} {self.last_name}'

    def mapper(self):
        return dict(
            id=self.id,
            name=self.name,
            last_name=self.last_name,
            identification=self.identification,
            gender=self.gender,
            age=self.age,
            phone=self.phone
        )


class Student(BaseModel):
    representative_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    expectations = models.TextField(
        null=True,
        blank=True
    )
    emergency_contact = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    observations = models.TextField(
        default='S/N',
        null=True,
        blank=True,
    )
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        null=False,
    )

    objects = StudentManager()

    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'{self.person.name} {self.person.last_name}'

    def get_representative(self):
        return f'{self.representative_name} - {self.emergency_contact}'

    def mapper(self):
        return dict(
            id=self.id,
            name=self.person.name,
            last_name=self.person.last_name,
            identification=self.person.identification,
            expectations=self.expectations,
            phone=self.person.phone,
            representative=self.get_representative()
        )


class Teacher(BaseModel):
    objective = models.TextField(
        default='S/N',
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=80,
        null=False,
        blank=False,
    )
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        null=False
    )

    objects = TeacherManager()

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f'{self.person.name} {self.person.last_name}'

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


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    # USERS
    class UserChoices(models.IntegerChoices):
        ADMINISTRATOR = 0
        TEACHER = 1
        STUDENT = 2

    username = models.CharField(
        'Nombre de Usuario',
        max_length=100,
        unique=True
    )
    email = models.EmailField(
        'Correo Electrónico',
        null=True,
        blank=True,
        unique=True
    )
    type = models.PositiveSmallIntegerField(
        choices=UserChoices.choices,
        null=False,
        blank=False
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

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return dict(
            refresh=str(refresh),
            access=str(refresh.access_token)
        )


class AuditUser(models.Model):

    # AUDIT TYPES
    class AuditTypesChoices(models.IntegerChoices):
        CREATE = 0
        LIST = 1
        UPDATE = 2
        DELETE = 3

    table = models.CharField(
        max_length=30,
        null=False,
        blank=False
    )
    fields_changed = models.JSONField(
        null=False,
        blank=False
    )
    record_id = models.IntegerField(
        null=False,
        blank=False
    )
    audit_type = models.PositiveIntegerField(
        choices=AuditTypesChoices.choices,
        null=False,
        blank=False
    )
    old_values = models.JSONField(
        null=True,
        blank=True
    )
    new_values = models.JSONField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )
    observations = models.TextField(
        null=True,
        blank=True
    )
    add_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    class Meta:
        db_table = 'audit_user'
        verbose_name = 'AuditUser'
        verbose_name_plural = 'AuditUsers'

    def mapper(self):
        return dict(
            id=self.id,
            add_by=self.add_by,
            table=self.table,
            fields_changed=self.fields,
            record_id=self.record_id,
            audit_type=self.audit_type,
            old_values=self.old_values,
            new_values=self.new_values,
            created_at=self.created_at,
            observations=self.observations
        )
