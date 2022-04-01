from rest_framework import routers

from .api.api_ac.viewsets import AcViewSet
from .api.api_team_ac.viewsets import TeamAcViewSet
from .api.api_team_detail_ac.viewsets import TeamDetailAcViewSet
from .api.api_rubric_ac.viewsets import RubricAcViewSet
from .api.api_rubric_detail_ac.viewsets import RubricDetailAcViewSet
from .api.api_student_evaluation_ac.viewsets import StudentEvaluationAcViewSet
from .api.api_student_evaluation_detail_ac.viewsets import StudentEvaluationDetailAcViewSet

router = routers.DefaultRouter()

router.register(
    r'ac',
    AcViewSet,
    basename='ac'
)
router.register(
    r'team-ac',
    TeamAcViewSet,
    basename='team_ac'
)
router.register(
    r'team-detail-ac',
    TeamDetailAcViewSet,
    basename='team_detail_ac'
)
router.register(
    r'rubric-ac',
    RubricAcViewSet,
    basename='rubric_ac'
)
router.register(
    r'rubric-detail-ac',
    RubricDetailAcViewSet,
    basename='rubric_detail_ac'
)
router.register(
    r'student-evaluation-ac',
    StudentEvaluationAcViewSet,
    basename='student_evaluation_ac'
)
router.register(
    r'student-evaluation-detail-ac',
    StudentEvaluationDetailAcViewSet,
    basename='student_evaluation_detail_ac'
)

urlpatterns = router.urls
