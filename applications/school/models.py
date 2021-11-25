from django.db import models

from applications.base.models import BaseModel
from applications.users.models import Teacher, Student
from applications.school.api.api_knowledge_area.managers import KnowledgeAreaManager
from applications.school.api.api_school_period.managers import SchoolPeriodManager
from applications.school.api.api_classroom.managers import ClassroomManager
from applications.school.api.api_asignature.managers import AsignatureManager
from applications.school.api.api_asignature_classroom.managers import AsignatureClassroomManager
from applications.school.api.api_glossary.managers import GlossaryManager
from applications.school.api.api_glossary_detail.managers import GlossaryDetailManager


# TODO: Crear una tabla de niveles para las tablas
#   Aula y Asignatura


class SchoolPeriod(BaseModel):
    class PeriodStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    name = models.CharField(
        'nombre',
        max_length=50,
        null=False,
        blank=False,
    )
    init_date = models.DateField(
        'fecha de inicio',
        null=False,
        blank=False
    )
    end_date = models.DateField(
        'fecha fin',
        null=False,
        blank=False
    )
    school_end_date = models.DateField(
        'fecha fin de clases',
        null=False,
        blank=False
    )
    state = models.PositiveSmallIntegerField(
        'estado',
        choices=PeriodStatus.choices,
        default=1,
        null=True,
        blank=True,
    )
    observations = models.TextField(
        'observaciones',
        default='S/N',
        null=True,
        blank=True,
    )

    objects = SchoolPeriodManager()

    class Meta:
        db_table = 'school_period'
        verbose_name = 'SchoolPeriod'
        verbose_name_plural = 'SchoolPeriods'
    
    def __str__(self):
        return f'{self.name}'

    def get_period_date(self):
        return f'{self.init_date} - {self.end_date}'
    

class KnowledgeArea(BaseModel):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    objective = models.TextField(
        default='S/N',
        null=True,
        blank=True
    )
    coordinator = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='coordinator',
        null=False,
        blank=False
    )
    sub_coordinator = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='sub_coordinator',
        null=False,
        blank=False
    )
    observations = models.TextField(
        'observaciones',
        default='S/N',
        null=True,
        blank=True,
    )

    teachers = models.ManyToManyField(
        Teacher,
        blank=True
    )

    objects = KnowledgeAreaManager()

    class Meta:
        db_table = 'knowledge_area'
        verbose_name = 'KnowledgeArea'
        verbose_name_plural = 'KnowledgeAreas'

    def __str__(self):
        return f'{self.name}'

    def get_coordinator(self):
        return f'{self.coordinator.person.name} {self.coordinator.person.last_name}'


class Classroom(BaseModel):

    class CurseLevelStatus(models.IntegerChoices):
        PRIMERO = 1
        SEGUNDO = 2
        TERCERO = 3

    class ClassroomStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    curse_level = models.PositiveSmallIntegerField(
        choices=CurseLevelStatus.choices,
        default=1,
        null=True,
        blank=False
    )
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        'estado',
        choices=ClassroomStatus.choices,
        default=1,
        null=True,
        blank=True,
    )

    school_period = models.ForeignKey(
        SchoolPeriod,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    students = models.ManyToManyField(
        Student,
        blank=True
    )

    objects = ClassroomManager()

    class Meta:
        db_table = 'classroom'
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'

    def __str__(self):
        return f'{self.name}'


class Asignature(BaseModel):

    class AsignatureStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    name = models.CharField(
        max_length=40,
        null=False,
        blank=False,
    )
    objective = models.TextField(
        null=True,
        blank=True
    )
    observations = models.TextField(
        default='S/N',
        null=True,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        'estado',
        choices=AsignatureStatus.choices,
        default=1,
        null=True,
        blank=True,
    )

    knowledge_area = models.ForeignKey(
        KnowledgeArea,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    classrooms = models.ManyToManyField(
        Classroom,
        through='AsignatureClassroom',
        blank=True
    )

    objects = AsignatureManager()

    class Meta:
        db_table = 'asignature'
        verbose_name = 'Asignature'
        verbose_name_plural = 'Asignatures'

    def __str__(self):
        return f'{self.name}'


class AsignatureClassroom(BaseModel):

    class AsignatureClassroomStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    asignature = models.ForeignKey(
        Asignature,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    observations = models.TextField(
        default='S/N',
        null=True,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        'estado',
        choices=AsignatureClassroomStatus.choices,
        default=1,
        null=True,
        blank=True,
    )

    objects = AsignatureClassroomManager()

    class Meta:
        db_table = 'asignature_classroom'
        verbose_name = 'AsignatureClassroom'
        verbose_name_plural = 'AsignaturesClassrooms'

    def __str__(self):
        return f'{self.classroom.name} - {self.asignature.name} -> ' \
               f'{self.teacher.person.name} {self.teacher.person.last_name}'


class Glossary(BaseModel):
    state = models.BooleanField(
        'Estado',
        default=False,
        null=False,
        blank=True
    )
    observations = models.TextField(
        'Observaciones',
        default='S/N',
        null=True,
        blank=True
    )

    asignature_classroom = models.ForeignKey(
        AsignatureClassroom,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = GlossaryManager()

    class Meta:
        db_table = 'glossary'
        verbose_name = 'Glossary'
        verbose_name_plural = 'Glossaries'


class GlossaryDetail(BaseModel):
    title = models.CharField(
        'Título',
        max_length=150,
        null=False,
        blank=False,
    )
    description = models.TextField(
        'descripción',
        null=False,
        blank=False
    )
    image = models.URLField(
        max_length=230,
        null=True,
        blank=True
    )
    url = models.URLField(
        max_length=230,
        null=True,
        blank=True
    )
    observation = models.TextField(
        'observación',
        default='S/N',
        null=True,
        blank=True
    )
    state = models.BooleanField(
        'estado',
        default=True,
        null=False,
        blank=True
    )

    glossary = models.ForeignKey(
        Glossary,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = GlossaryDetailManager()

    class Meta:
        db_table = 'glossary_detail'
        verbose_name = 'Glossary Detail'
        verbose_name_plural = 'Glossary Details'
