from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

from applications.base.models import BaseModel
from applications.users.managers import UserManager
from applications.users.api.api_student.managers import StudentManager
from applications.users.api.api_teacher.managers import TeacherManager
from applications.users.api.api_person.managers import PersonManager
from applications.users.api.api_conversation.managers import ConversationManager
from applications.users.api.api_conversation_detail.managers import ConversationDetailManager


class Person(BaseModel):

    # GENDERS
    class GenderChoices(models.IntegerChoices):
        FEMENINO = 1
        MASCULINO = 2
        OTRO = 3

    class IdentificationChoices(models.IntegerChoices):
        CI = 1
        OTHER = 2

    identification_type = models.PositiveIntegerField(
        'tipo de identificación',
        choices=IdentificationChoices.choices,
        default=0,
        null=False,
        blank=False,
    )
    identification = models.CharField(
        'identificación',
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )
    name = models.CharField(
        'nombre',
        max_length=80,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        'apellido',
        max_length=100,
        null=False,
        blank=False
    )
    gender = models.PositiveSmallIntegerField(
        'género',
        choices=GenderChoices.choices,
        null=False,
        blank=False,
    )
    age = models.PositiveIntegerField(
        'edad',
        null=False,
        blank=False
    )
    phone = models.CharField(
        'teléfono',
        max_length=20,
        null=False,
        blank=False,
    )

    objects = PersonManager()

    class Meta:
        db_table = 'person'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f'{self.identification} - {self.name} {self.last_name}'

    def full_name(self):
        return f'{self.name} {self.last_name}'


class Student(BaseModel):

    representative_name = models.CharField(
        'nombre del representante',
        max_length=100,
        null=True,
        blank=True
    )
    expectations = models.JSONField(
        'expectativas',
        default=dict,
        null=True,
        blank=True
    )
    emergency_contact = models.CharField(
        'contacto de emergencia',
        max_length=20,
        null=True,
        blank=True,
    )
    observations = models.JSONField(
        'observaciones',
        default=dict,
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
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return f'{self.person.name} {self.person.last_name}'


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


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    # USERS
    class UserChoices(models.IntegerChoices):
        ADMINISTRATOR = 0
        TEACHER = 1
        STUDENT = 2

    username = models.CharField(
        'nombre de usuario',
        max_length=100,
        unique=True
    )
    email = models.EmailField(
        'correo electrónico',
        null=True,
        blank=True,
        unique=True
    )
    type = models.PositiveSmallIntegerField(
        'tipo de usuario',
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

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return dict(
            refresh=str(refresh),
            access=str(refresh.access_token)
        )

    def __str__(self):
        try:
            return f'{self.person.name} {self.person.last_name}'
        except:
            return None

    def get_username(self):
        return self.username


class Conversation(BaseModel):

    blocked = models.BooleanField(
        'Bloqueado',
        default=False,
        null=False,
        blank=True
    )

    first_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='first_user',
        null=False,
        blank=False
    )
    second_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='second_user',
        null=False,
        blank=False
    )

    objects = ConversationManager()

    class Meta:
        db_table = 'conversation'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'

    def __str__(self):
        return f'Conversación entre {self.first_user.person.name} {self.first_user.person.last_name} - ' \
               f'{self.second_user.person.name} {self.second_user.person.last_name}'


class Conversation_Detail(BaseModel):

    class MessageStateChoices(models.IntegerChoices):
        NOT_VIEW = 0
        VIEW = 1

    detail = models.TextField(
        'Mensaje',
        null=False,
        blank=False
    )
    send_date = models.DateTimeField(
        'Fecha de Creación',
        auto_now_add=True,
        auto_now=False,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        'Estado',
        choices=MessageStateChoices.choices,
        default=0,
        null=False,
        blank=True
    )
    blocked = models.BooleanField(
        'Bloqueado',
        default=False,
        null=True,
        blank=True
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = ConversationDetailManager()

    class Meta:
        db_table = 'conversation_detail'
        verbose_name = 'Conversation Detail'
        verbose_name_plural = 'Conversation Details'

    def __str__(self):
        return self.detail


# DEPRECATED MODEL
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
    new_values = models.JSONField(
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
    fields_changed = models.JSONField(
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
            fields_changed=self.fields_changed,
            record_id=self.record_id,
            audit_type=self.audit_type,
            old_values=self.old_values,
            new_values=self.new_values,
            created_at=self.created_at,
            observations=self.observations
        )
