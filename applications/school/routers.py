from rest_framework import routers

from applications.school.api.api_school_period.viewsets import SchoolPeriodViewSet
from applications.school.api.api_knowledge_area.viewsets import KnowledgeAreaViewSet
from applications.school.api.api_classroom.viewsets import ClassroomViewSet
from applications.school.api.api_asignature.viewsets import AsignatureViewSet
from applications.school.api.api_asignature_classroom.viewsets import AsignatureClassroomViewSet

router = routers.DefaultRouter()

router.register(
    r'school-period',
    SchoolPeriodViewSet,
    basename='school_period'
)
router.register(
    r'knowledge-area',
    KnowledgeAreaViewSet,
    basename='knowledge_area'
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
    r'asignature-classroom',
    AsignatureClassroomViewSet,
    basename='asignature_classroom'
)

urlpatterns = router.urls
