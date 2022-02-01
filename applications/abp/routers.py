from rest_framework import routers

from applications.abp.api.api_abp.viewsets import AbpViewSet
from applications.abp.api.api_team_abp.viewsets import TeamAbpViewSet
from applications.abp.api.api_team_detail_abp.viewsets import TeamDetailAbpViewSet
from applications.abp.api.api_rubric_abp.viewsets import RubricAbpViewSet
from applications.abp.api.api_rubric_detail_abp.viewsets import RubricDetailAbpViewSet
from applications.abp.api.api_evaluation_abp.viewsets import EvaluationAbpViewSet
from applications.abp.api.api_evaluation_detail_abp.viewsets import EvaluationDetailAbpViewSet


router = routers.DefaultRouter()

router.register(
    r'abp',
    AbpViewSet,
    basename='abp'
)
router.register(
    r'team-abp',
    TeamAbpViewSet,
    basename='team_abp'
)
router.register(
    r'team-detail-abp',
    TeamDetailAbpViewSet,
    basename='team_detail_abp'
)
router.register(
    r'rubric-abp',
    RubricAbpViewSet,
    basename='rubric_abp'
)
router.register(
    r'rubric-detail-abp',
    RubricDetailAbpViewSet,
    basename='rubric_detail_abp'
)
router.register(
    r'evaluation-abp',
    EvaluationAbpViewSet,
    basename='evaluation_abp'
)
router.register(
    r'evaluation-detail-abp',
    EvaluationDetailAbpViewSet,
    basename='evaluation_detail_abp'
)

urlpatterns = router.urls
