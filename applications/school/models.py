from django.db import models

from applications.base.models import BaseModel
from applications.users.models import Teacher, Student
from applications.school.api_knowledge_area.managers import KnowledgeAreaManager


class SchoolPeriod(BaseModel):

    class PeriodStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    init_date = models.DateTimeField(
        null=False,
        blank=False
    )
    end_date = models.DateTimeField(
        null=False,
        blank=False
    )
    school_end_date = models.DateTimeField(
        null=False,
        blank=False
    )
    state = models.PositiveSmallIntegerField(
        choices=PeriodStatus.choices,
        default=1,
        null=False,
        blank=False,
    )
    observations = models.TextField(
        default='S/N',
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'school_period'
        verbose_name = 'SchoolPeriod'
        verbose_name_plural = 'SchoolPeriods'

    def __str__(self):
        return f'{self.name}'

    def get_period_date(self):
        return f'{self.init_date} - {self.end_date}'

    def mapper(self):
        return dict(
            name=self.name,
            init_date=self.init_date,
            end_date=self.end_date,
            school_end_date=self.school_end_date,
            state=self.state.__str__(),
            observations=self.observations
        )


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

    def get_sub_coordinator(self):
        return f'{self.sub_coordinator.person.name} {self.sub_coordinator.person.last_name}'


class Classroom(BaseModel):

    class GradeChoices(models.IntegerChoices):
        PRIMERO = 1
        SEGUNDO = 2
        TERCERO = 3

    name = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False
    )
    grade_level = models.PositiveSmallIntegerField(
        choices=GradeChoices.choices,
        null=False,
        blank=False
    )
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True
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

    class Meta:
        db_table = 'classroom'
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'

    def __str__(self):
        return f'{self.name}'


class Asignature(BaseModel):
    name = models.CharField(
        max_length=40,
        null=False,
        blank=False,
        unique=True
    )
    objective = models.TextField(
        null=True,
        blank=True
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

    class Meta:
        db_table = 'asignature'
        verbose_name = 'Asignature'
        verbose_name_plural = 'Asignatures'

    def __str__(self):
        return f'{self.name}'


class AsignatureClassroom(BaseModel):
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
    observation = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'asignature_classroom'
        verbose_name = 'AsignatureClassroom'
        verbose_name_plural = 'AsignaturesClassrooms'

    def __str__(self):
        return f'{self.classroom.name} - {self.asignature.name} -> ' \
               f'{self.teacher.person.name} {self.teacher.person.last_name}'
