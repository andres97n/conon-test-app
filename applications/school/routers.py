from rest_framework import routers

from applications.school.api_school_period.viewsets import SchoolPeriodViewSet
from applications.school.api_knowledge_area.viewsets import KnowledgeAreaViewSet
from applications.school.api_classroom.viewsets import ClassroomViewSet

router = routers.DefaultRouter()

router.register(
    r'school-period',
    SchoolPeriodViewSet,
    basename='school-period'
)
router.register(
    r'knowledge-area',
    KnowledgeAreaViewSet,
    basename='knowledge-area'
)
router.register(
    r'classroom',
    ClassroomViewSet,
    basename='classroom'
)

urlpatterns = router.urls
