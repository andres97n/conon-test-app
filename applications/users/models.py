from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from applications.users.managers import UserManager


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_state = models.CharField(max_length=1, default='A')

    class Meta:
        abstract = True


class Person(BaseModel):
    # GENDERS
    class GenderChoices(models.IntegerChoices):
        FEMININE = 0
        MASCULINE = 1
        OTHER = 2

    identification = models.CharField(
        max_length=30,
        unique=True,
        blank=False
    )
    name = models.CharField(
        max_length=50,
        blank=False
    )
    last_name = models.CharField(
        max_length=80,
        blank=False
    )
    gender = models.PositiveIntegerField(
        blank=True,
        choices=GenderChoices.choices
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
        return f'{self.name} {self.last_name}'

    def mapper(self):
        return dist(
            id=self.id,
            name=self.person.name,
            last_name=self.person.last_name,
            identification=self.person.identification,
            gender=self.gender,
            age=self.age,
            phone=self.person.phone
        )


class Student(BaseModel):
    representative_name = models.CharField(
        max_length=50,
        blank=True
    )
    expectations = models.TextField(
        null=True,
        blank=True
    )
    emergency_contact = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )
    observations = models.TextField(
        null=True,
        blank=True
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=False
    )

    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'{self.person.name} {self.person.last_name}'

    def get_representative(self):
        return f'{self.representative_name} - {self.emergency_contact}'

    def mapper(self):
        return dist(
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
        blank=True
    )
    title = models.CharField(
        max_length=40,
        null=False
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=False
    )

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f'{self.person.name} {self.person.last_name}'

    def mapper(self):
        return dist(
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
        max_length=30,
        unique=True
    )
    email = models.EmailField(
        'Correo Electrónico',
        null=True,
        blank=True,

    )
    type = models.PositiveIntegerField(
        choices=UserChoices.choices,
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


class AuditUser(models.Model):
    table = models.CharField(
        max_length=30,
        null=False
    )
    fields = models.JSONField(
        null=False
    )
    record_id = models.IntegerField(
        null=False
    )
    old_values = models.JSONField(
        null=False
    )
    new_values = models.JSONField(
        null=False
    )
    created_at = models.JSONField(
        null=False
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
        return dist(
            id=self.id,
            add_by=self.add_by,
            table=self.table,
            fields=self.fields,
            old_values=self.old_values,
            new_values=self.new_values,
            created_at=self.created_at,
            observations=self.observations
        )
