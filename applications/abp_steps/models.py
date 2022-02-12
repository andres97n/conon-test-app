from django.db import models

from applications.base.models import BaseModel
from applications.users.models import User
from applications.abp.models import TeamAbp, TeamDetailAbp
from applications.abp_steps.api.api_opinion_step_one_abp.managers import OpinionStepOneAbpManager
from applications.abp_steps.api.api_interaction_step_one_abp.managers import \
    InteractionStepOneAbpManager
from applications.abp_steps.api.api_question_step_one_abp.managers import QuestionStepOneAbpManager
from applications.abp_steps.api.api_answer_step_one_abp.managers import AnswerStepOneAbpManager


class OpinionStepOneAbp(BaseModel):
    opinion = models.TextField(
        null=False,
        blank=False
    )
    active = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    team_detail_abp = models.ForeignKey(
        TeamDetailAbp,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = OpinionStepOneAbpManager()

    def __str__(self):
        return self.opinion

    class Meta:
        db_table = 'opinion_step_one_abp'
        verbose_name = 'OpinionStepOneAbp'


class InteractionStepOneAbp(BaseModel):
    class InteractionStepOneAbpStatus(models.IntegerChoices):
        NOTHING = 0
        DISAGREE = 1
        AGREE = 2

    opinion_interaction = models.PositiveSmallIntegerField(
        choices=InteractionStepOneAbpStatus.choices,
        default=0,
        null=False,
        blank=False
    )
    active = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    objects = InteractionStepOneAbpManager()

    opinion_step_one_abp = models.ForeignKey(
        OpinionStepOneAbp,
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

    def __str__(self):
        return self.opinion_interaction

    class Meta:
        db_table = 'interaction_step_one_abp'
        verbose_name = 'InteractionStepOneAbp'


class QuestionStepOneAbp(BaseModel):
    moderator_question = models.CharField(
        max_length=250,
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

    objects = QuestionStepOneAbpManager()

    def __str__(self):
        return self.moderator_question

    class Meta:
        db_table = 'question_step_one_abp'
        verbose_name = 'QuestionStepOneAbp'


class AnswerStepOneAbp(BaseModel):
    teacher_answer = models.TextField(
        null=False,
        blank=False
    )
    active = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    question_step_one_abp = models.ForeignKey(
        QuestionStepOneAbp,
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

    objects = AnswerStepOneAbpManager()

    def __str__(self):
        return self.teacher_answer

    class Meta:
        db_table = 'answer_step_one_abp'
        verbose_name = 'AnswerStepOneAbp'
