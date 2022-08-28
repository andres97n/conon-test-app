from django.db import models

from applications.base.models import BaseModel, BaseModelActive
from applications.topic.models import Topic
from applications.users.models import User
from applications.ac.api.api_ac.managers import AcManager
from applications.ac.api.api_team_ac.managers import TeamAcManager
from applications.ac.api.api_team_detail_ac.managers import TeamDetailAcManager
from applications.ac.api.api_rubric_ac.managers import RubricAcManager
from applications.ac.api.api_rubric_detail_ac.managers import RubricDetailAcManager
from applications.ac.api.api_student_evaluation_ac.managers import StudentEvaluationAcManager
from applications.ac.api.api_student_evaluation_detail_ac.managers import \
    StudentEvaluationDetailAcManager


class Ac(BaseModel):
    class AcStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    real_problem = models.TextField(null=False, blank=False)
    context_video = models.URLField(null=True, blank=True)
    path_reference = models.URLField(null=True, blank=True)
    context_audio = models.JSONField(
        null=True,
        blank=True,
        default=dict
    )
    state = models.PositiveSmallIntegerField(
        choices=AcStatus.choices,
        default=1,
        null=False,
        blank=True
    )

    topic = models.OneToOneField(
        Topic,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    objects = AcManager()

    def __str__(self):
        return self.topic.title

    class Meta:
        db_table = 'ac'
        verbose_name = 'AC'


class TeamAc(BaseModelActive):
    class TeamStateStatus(models.IntegerChoices):
        FINISHED = 0
        WORKING = 1

    team_state = models.PositiveSmallIntegerField(
        choices=TeamStateStatus.choices,
        default=1,
        null=False,
        blank=True
    )
    observations = models.TextField(null=True, blank=True)

    ac = models.ForeignKey(
        Ac,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    objects = TeamAcManager()

    class Meta:
        db_table = 'team_ac'
        verbose_name = 'TeamAc'
        verbose_name_plural = 'TeamsAc'

    def __str__(self):
        return self.ac.id


class TeamDetailAc(BaseModelActive):
    class TeamDetailTypeStatus(models.IntegerChoices):
        COORDINATOR = 1
        SPOKESMAN = 2
        ORGANIZER = 3
        SECRETARY = 4

    role_type = models.PositiveSmallIntegerField(
        choices=TeamDetailTypeStatus.choices,
        null=False,
        blank=False
    )

    team_ac = models.ForeignKey(
        TeamAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = TeamDetailAcManager()

    class Meta:
        db_table = 'team_detail_ac'
        verbose_name = 'TeamDetailAc'
        verbose_name_plural = 'TeamDetailsAc'

    def __str__(self):
        return self.owner.__str__()


class RubricAc(BaseModel):
    class RubricAcStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    description_rubric = models.TextField(null=True, blank=True)
    ac_final_value = models.FloatField(
        default=0,
        null=False,
        blank=False
    )
    observations = models.TextField(null=True, blank=True)
    state = models.PositiveSmallIntegerField(
        choices=RubricAcStatus.choices,
        default=1,
        null=False,
        blank=True
    )

    ac = models.ForeignKey(
        Ac,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = RubricAcManager()

    class Meta:
        db_table = 'rubric_ac'
        verbose_name = 'RubricAc'
        verbose_name_plural = 'RubricsAc'

    def __str__(self):
        return self.description_rubric


class RubricDetailAc(BaseModelActive):
    detail_title = models.CharField(
        max_length=250,
        null=False,
        blank=False
    )
    detail_description = models.TextField(null=True, blank=True)
    percentage_grade = models.FloatField(null=False, blank=False)
    rating_value = models.FloatField(
        default=0,
        null=False,
        blank=False
    )
    observations = models.TextField(null=True, blank=True)

    rubric_ac = models.ForeignKey(
        RubricAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = RubricDetailAcManager()

    class Meta:
        db_table = 'rubric_detail_ac'
        verbose_name = 'RubricDetailAc'
        verbose_name_plural = 'RubricDetailsAc'

    def __str__(self):
        return self.detail_title


class StudentEvaluationAc(BaseModel):
    class StudentEvaluationAcStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    description = models.TextField(null=True, blank=True)
    final_value = models.FloatField(null=False, blank=False)
    observations = models.TextField(null=True, blank=True)
    state = models.PositiveSmallIntegerField(
        choices=StudentEvaluationAcStatus.choices,
        null=False,
        blank=False
    )

    rubric_ac = models.ForeignKey(
        RubricAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = StudentEvaluationAcManager()

    class Meta:
        db_table = 'student_evaluation_ac'
        verbose_name = 'StudentEvaluationAc'
        verbose_name_plural = 'StudentEvaluationsAc'

    def __str__(self):
        return self.final_value


class StudentEvaluationDetailAc(BaseModelActive):
    class StudentEvaluationAcTypeStatus(models.IntegerChoices):
        AUTOEVALUATION = 1
        COEVALUATION = 2
        OTHER = 3

    evaluation_type = models.PositiveSmallIntegerField(
        choices=StudentEvaluationAcTypeStatus.choices,
        null=False,
        blank=False
    )
    detail_value = models.FloatField(null=False, blank=False)
    detail_body = models.JSONField(

        null=True,
        blank=True,
        default=dict
    )

    rubric_detail_ac = models.ForeignKey(
        RubricDetailAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    student_evaluation_ac = models.ForeignKey(
        StudentEvaluationAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = StudentEvaluationDetailAcManager()

    class Meta:
        db_table = 'student_evaluation_detail_ac'
        verbose_name = 'StudentEvaluationDetailAc'
        verbose_name_plural = 'StudentEvaluationDetailsAc'

    def __str__(self):
        return self.detail_value
