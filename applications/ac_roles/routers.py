from rest_framework import routers

from .api.api_coordinator_strategy_ac.viewsets import CoordinatorStrategyAcViewSet
from .api.api_member_performance_coordinator_ac.viewsets import MemberPerformanceCoordinatorAcViewSet
from .api.api_problem_resolution_group_ac.viewsets import ProblemResolutionGroupAcViewSet
from .api.api_organizer_action_ac.viewsets import OrganizerActionAcViewSet
from .api.api_assign_activity_organizer_ac.viewsets import AssignActivityOrganizerAcViewSet
from .api.api_describe_understanding_organizer_ac.viewsets import DescribeUnderstandingOrganizerAcViewSet
from .api.api_spokesman_question_ac.viewsets import SpokesmanQuestionAcViewSet
from .api.api_activity_description_spokesman_ac.viewsets import ActivityDescriptionSpokesmanAcViewSet
from .api.api_performance_description_spokesman_ac.viewsets import PerformanceDescriptionSpokesmanAcViewSet
from .api.api_secretary_information_ac.viewsets import SecretaryInformationAcViewSet
from .api.api_featured_information_secretary_ac.viewsets import FeaturedInformationSecretaryAcViewSet
from .api.api_teacher_answer_ac.viewsets import TeacherAnswerAcViewSet
from .api.api_teacher_answer_description_secretary_ac.viewsets import TeacherAnswerDescriptionSecretaryAcViewSet

router = routers.DefaultRouter()

router.register(
    r'coordinator-strategy-ac',
    CoordinatorStrategyAcViewSet,
    basename='coordinator_strategy_ac'
)
router.register(
    r'member-performance-coordinator-ac',
    MemberPerformanceCoordinatorAcViewSet,
    basename='member_performance_coordinator_ac'
)
router.register(
    r'problem-resolution-group-ac',
    ProblemResolutionGroupAcViewSet,
    basename='problem_resolution_group_ac'
)
router.register(
    r'organizer-action-ac',
    OrganizerActionAcViewSet,
    basename='organizer_action_ac'
)
router.register(
    r'assign-activity-organizer-ac',
    AssignActivityOrganizerAcViewSet,
    basename='assign_activity_organizer_ac'
)
router.register(
    r'describe-understanding-organizer-ac',
    DescribeUnderstandingOrganizerAcViewSet,
    basename='describe_understanding_organizer_ac'
)
router.register(
    r'spokesman-question-ac',
    SpokesmanQuestionAcViewSet,
    basename='spokesman_question_ac'
)
router.register(
    r'activity-description-spokesman-ac',
    ActivityDescriptionSpokesmanAcViewSet,
    basename='activity_description_spokesman_ac'
)
router.register(
    r'performance-description-spokesman-ac',
    PerformanceDescriptionSpokesmanAcViewSet,
    basename='performance_description_spokesman_ac'
)
router.register(
    r'secretary-information-ac',
    SecretaryInformationAcViewSet,
    basename='secretary_information_ac'
)
router.register(
    r'featured-information-secretary-ac',
    FeaturedInformationSecretaryAcViewSet,
    basename='featured_information_secretary_ac'
)
router.register(
    r'teacher-answer-ac',
    TeacherAnswerAcViewSet,
    basename='teacher_answer_ac'
)
router.register(
    r'teacher-answer-description-secretary-ac',
    TeacherAnswerDescriptionSecretaryAcViewSet,
    basename='teacher_answer_description_secretary_ac'
)

urlpatterns = router.urls
