from rest_framework import routers

from applications.school.api_school_period.viewsets import SchoolPeriodViewSet
from applications.school.api_knowledge_area.viewsets import KnowledgeAreaViewSet
from applications.school.api_classroom.viewsets import ClassroomViewSet
from applications.school.api_asignature.viewsets import AsignatureViewSet
from applications.school.api_asignature_classroom.viewsets import AsignatureClassroomViewSet

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
router.register(
    r'asignature',
    AsignatureViewSet,
    basename='asignature'
)
router.register(
    r'asignature_classroom',
    AsignatureClassroomViewSet,
    basename='asignature_classroom'
)

urlpatterns = router.urls
