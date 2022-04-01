from django.db import models

from applications.base.models import BaseModel
from applications.topic.models import Topic
from applications.users.models import User
from applications.abp.api.api_abp.managers import AbpManager
from applications.abp.api.api_team_abp.managers import TeamAbpManager
from applications.abp.api.api_team_detail_abp.managers import TeamDetailAbpManager
from applications.abp.api.api_rubric_abp.managers import RubricAbpManager
from applications.abp.api.api_rubric_detail_abp.managers import RubricDetailAbpManager
from applications.abp.api.api_evaluation_abp.managers import EvaluationAbpManager
from applications.abp.api.api_evaluation_detail_abp.managers import EvaluationDetailAbpManager


class Abp(BaseModel):
    class AbpStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    problem = models.TextField(
        null=False,
        blank=False
    )
    oral_explication = models.JSONField(
        null=True,
        blank=True
    )
    """
        {
            name: '',
            url: '',
            size: 0
        }
    """
    descriptive_image = models.JSONField(
        null=True,
        blank=True
    )
    reference_url = models.TextField(
        null=True,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        choices=AbpStatus.choices,
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

    objects = AbpManager()

    def __str__(self):
        return self.topic.title

    class Meta:
        db_table = 'abp'
        verbose_name = 'ABP'


class TeamAbp(BaseModel):
    class TeamAbpStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    class StepTeamAbpStatus(models.IntegerChoices):
        STEP_ONE = 1
        STEP_TWO = 2
        STEP_THREE = 3
        STEP_FOUR = 4
        STEP_FIVE = 5
        STEP_SIX = 6
        STEP_SEVEN = 7
        STEP_EIGHT = 8
        STEP_NINE = 9

    step = models.PositiveIntegerField(
        choices=StepTeamAbpStatus.choices,
        default=1,
        null=False,
        blank=False
    )
    observations = models.TextField(
        null=True,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        choices=TeamAbpStatus.choices,
        default=1,
        null=False,
        blank=True
    )

    abp = models.ForeignKey(
        Abp,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = TeamAbpManager()

    class Meta:
        db_table = 'team_abp'
        verbose_name = 'TeamAbp'
        verbose_name_plural = 'TeamsAbp'

    def __str__(self):
        return self.abp.id


class TeamDetailAbp(BaseModel):
    is_moderator = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )
    active = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    team_abp = models.ForeignKey(
        TeamAbp,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = TeamDetailAbpManager()

    class Meta:
        db_table = 'team_detail_abp'
        verbose_name = 'TeamDetailAbp'
        verbose_name_plural = 'TeamDetailsAbp'

    def __str__(self):
        return self.user.person.__str__()


class RubricAbp(BaseModel):
    class RubricAbpStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    description_rubric = models.TextField(
        null=True,
        blank=True
    )
    abp_final_value = models.FloatField(
        default=0,
        null=False,
        blank=False
    )
    observations = models.TextField(
        null=True,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        choices=RubricAbpStatus.choices,
        default=1,
        null=False,
        blank=True
    )

    abp = models.OneToOneField(
        Abp,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = RubricAbpManager()

    class Meta:
        db_table = 'rubric_abp'
        verbose_name = 'RubricAbp'
        verbose_name_plural = 'RubricsAbp'

    def __str__(self):
        return self.description_rubric


class RubricDetailAbp(BaseModel):
    title_detail = models.CharField(
        max_length=250,
        null=False,
        blank=False
    )
    description_detail = models.TextField(
        null=True,
        blank=True
    )
    grade_percentage = models.FloatField(
        null=False,
        blank=False
    )
    rating_value = models.FloatField(
        default=0,
        null=False,
        blank=False
    )
    observations_detail = models.TextField(
        null=True,
        blank=True
    )
    active = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    rubric_abp = models.ForeignKey(
        RubricAbp,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = RubricDetailAbpManager()

    class Meta:
        db_table = 'rubric_detail_abp'
        verbose_name = 'RubricDetailAbp'
        verbose_name_plural = 'RubricDetailsAbp'

    def __str__(self):
        return self.title_detail


class EvaluationAbp(BaseModel):
    class EvaluationAbpStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    description = models.TextField(
        null=True,
        blank=True
    )
    final_grade = models.FloatField(
        default=0,
        null=False,
        blank=False
    )
    observations = models.TextField(
        null=True,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        choices=EvaluationAbpStatus.choices,
        default=1,
        null=False,
        blank=True
    )

    abp = models.ForeignKey(
        Abp,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    team_detail_abp = models.ForeignKey(
        TeamDetailAbp,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = EvaluationAbpManager()

    class Meta:
        db_table = 'evaluation_abp'
        verbose_name = 'EvaluationAbp'
        verbose_name_plural = 'EvaluationsAbp'

    def __str__(self):
        return self.final_grade


class EvaluationDetailAbp(BaseModel):
    title_evaluation_detail = models.CharField(
        max_length=250,
        null=False,
        blank=False
    )
    evaluation_description = models.TextField(null=True, blank=True)
    grade_percentage = models.FloatField(
        default=0,
        null=False,
        blank=False
    )
    detail_body = models.JSONField(
        null=True,
        blank=True,
        default=dict
    )
    rating_value = models.FloatField(
        default=0,
        null=False,
        blank=False
    )
    active = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    evaluation_abp = models.ForeignKey(
        EvaluationAbp,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = EvaluationDetailAbpManager()

    class Meta:
        db_table = 'evaluation_detail_abp'
        verbose_name = 'EvaluationDetailAbp'
        verbose_name_plural = 'EvaluationDetailsAbp'

    def __str__(self):
        return self.rating_value
