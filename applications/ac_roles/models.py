from django.db import models

from applications.base.models import BaseModelActive
from applications.ac.models import TeamAc, TeamDetailAc
from applications.users.models import Teacher

from .api.api_coordinator_strategy_ac.managers import CoordinatorStrategyAcManager
from .api.api_member_performance_coordinator_ac.managers import MemberPerformanceCoordinatorAcManager
from .api.api_problem_resolution_group_ac.managers import ProblemResolutionGroupAcManager
from .api.api_organizer_action_ac.managers import OrganizerActionAcManager
from .api.api_assign_activity_organizer_ac.managers import AssignActivityOrganizerAcManager
from .api.api_describe_understanding_organizer_ac.managers import DescribeUnderstandingOrganizerAcManager
from .api.api_spokesman_question_ac.managers import SpokesmanQuestionAcManager
from .api.api_activity_description_spokesman_ac.managers import ActivityDescriptionSpokesmanAcManager
from .api.api_performance_description_spokesman_ac.managers import PerformanceDescriptionSpokesmanAcManager
from .api.api_secretary_information_ac.managers import SecretaryInformationAcManager
from .api.api_featured_information_secretary_ac.managers import FeaturedInformationSecretaryAcManager
from .api.api_teacher_answer_ac.managers import TeacherAnswerAcManager
from .api.api_teacher_answer_description_secretary_ac.managers import TeacherAnswerDescriptionSecretaryAcManager


class CoordinatorStrategyAc(BaseModelActive):
    strategy = models.TextField(null=False, blank=False)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = CoordinatorStrategyAcManager()

    def __str__(self):
        return self.strategy

    class Meta:
        db_table = 'coordinator_strategy_ac'
        verbose_name = 'CoordinatorStrategyAc'
        verbose_name_plural = 'CoordinatorStrategiesAc'


class MemberPerformanceCoordinatorAc(BaseModelActive):
    member_assessment = models.FloatField(null=False, blank=False)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='team_detail_member_performance_ac',
        null=False,
        blank=False
    )
    member_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='member_member_performance_ac',
        null=False,
        blank=False
    )

    objects = MemberPerformanceCoordinatorAcManager()

    def __str__(self):
        return self.member_assessment

    class Meta:
        db_table = 'member_performance_coordinator_ac'
        verbose_name = 'MemberPerformanceCoordinatorAc'
        verbose_name_plural = 'MemberPerformancesCoordinatorAc'


class ProblemResolutionGroupAc(BaseModelActive):
    problem_resolution = models.TextField(null=False, blank=False)
    references_images = models.JSONField(null=False, blank=True, default=dict)
    observations = models.TextField(null=True, blank=True, default='')

    team_ac = models.ForeignKey(
        TeamAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = ProblemResolutionGroupAcManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'problem_resolution_group_ac'
        verbose_name = 'ProblemResolutionGroupAc'
        verbose_name_plural = 'ProblemResolutionsGroupAc'


class OrganizerActionAc(BaseModelActive):
    action = models.TextField(null=False, blank=False)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = OrganizerActionAcManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'organizer_action_ac'
        verbose_name = 'OrganizerActionAc'
        verbose_name_plural = 'OrganizerActionsAc'


class AssignActivityOrganizerAc(BaseModelActive):
    member_activity = models.TextField(null=False, blank=False)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='team_detail_assign_organizer_ac',
        null=False,
        blank=False
    )
    member_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='member_assign_organizer_ac',
        null=False,
        blank=False
    )

    objects = AssignActivityOrganizerAcManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'assign_activity_organizer_ac'
        verbose_name = 'AssignActivityOrganizerAc'
        verbose_name_plural = 'AssignActivitiesOrganizerAc'


class DescribeUnderstandingOrganizerAc(BaseModelActive):
    member_assessment = models.IntegerField(null=False, blank=False, default=0)
    understanding = models.TextField(null=False, blank=False)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='team_detail_describe_understanding_ac',
        null=False,
        blank=False
    )
    member_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='member_describe_understanding_ac',
        null=False,
        blank=False
    )

    objects = DescribeUnderstandingOrganizerAcManager()

    def __str__(self):
        return self.member_assessment

    class Meta:
        db_table = 'describe_understanding_organizer_ac'
        verbose_name = 'DescribeUnderstandingOrganizerAc'


class SpokesmanQuestionAc(BaseModelActive):
    spokesman_question = models.CharField(null=False, blank=False, max_length=255)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = SpokesmanQuestionAcManager()

    def __str__(self):
        return self.spokesman_question

    class Meta:
        db_table = 'spokesman_question_ac'
        verbose_name = 'SpokesmanQuestionAc'
        verbose_name_plural = 'SpokesmanQuestionsAc'


class ActivityDescriptionSpokesmanAc(BaseModelActive):
    activity_description = models.TextField(null=False, blank=False)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    member_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='member_performance_description_ac',
        null=False,
        blank=False
    )

    objects = ActivityDescriptionSpokesmanAcManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'activity_description_spokesman_ac'
        verbose_name = 'ActivityDescriptionSpokesmanAc'
        verbose_name_plural = 'ActivityDescriptionsSpokesmanAc'


class PerformanceDescriptionSpokesmanAc(BaseModelActive):
    performance_description = models.TextField(null=False, blank=False)
    oral_description = models.JSONField(null=False, blank=True, default=dict)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='team_detail_performance_description_ac',
        null=False,
        blank=False
    )

    objects = PerformanceDescriptionSpokesmanAcManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'performance_description_spokesman_ac'
        verbose_name = 'PerformanceDescriptionSpokesmanAc'
        verbose_name_plural = 'PerformanceDescriptionsSpokesmanAc'


class SecretaryInformationAc(BaseModelActive):
    external_path = models.URLField(null=False, blank=False)

    team_ac = models.ForeignKey(
        TeamAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = SecretaryInformationAcManager()

    def __str__(self):
        return self.external_path

    class Meta:
        db_table = 'secretary_information_ac'
        verbose_name = 'SecretaryInformationAc'


class FeaturedInformationSecretaryAc(BaseModelActive):
    external_path = models.URLField(null=False, blank=False)
    description_path = models.TextField(null=False, blank=False)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='team_detail_featured_information_ac',
        null=False,
        blank=False
    )
    member_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        related_name='member_featured_information_ac',
        null=False,
        blank=False
    )

    objects = FeaturedInformationSecretaryAcManager()

    def __str__(self):
        return self.external_path

    class Meta:
        db_table = 'featured_information_secretary_ac'
        verbose_name = 'FeaturedInformationSecretaryAc'


class TeacherAnswerAc(BaseModelActive):
    teacher_answer = models.TextField(null=False, blank=False)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    spokesman_question_ac = models.ForeignKey(
        SpokesmanQuestionAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = TeacherAnswerAcManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'teacher_answer_ac'
        verbose_name = 'TeacherAnswerAc'
        verbose_name_plural = 'TeacherAnswersAc'


class TeacherAnswerDescriptionSecretaryAc(BaseModelActive):
    teacher_answer_description = models.TextField(null=False, blank=False)

    team_detail_ac = models.ForeignKey(
        TeamDetailAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    teacher_answer_ac = models.ForeignKey(
        TeacherAnswerAc,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = TeacherAnswerDescriptionSecretaryAcManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'teacher_answer_description_secretary_ac'
        verbose_name = 'TeacherAnswerDescriptionSecretaryAc'
        verbose_name_plural = 'TeacherAnswerDescriptionsSecretaryAc'
