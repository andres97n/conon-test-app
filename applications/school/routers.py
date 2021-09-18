from rest_framework import routers

from applications.school.api_knowledge_area.viewsets import KnowledgeAreaViewSet

router = routers.DefaultRouter()

router.register(
    r'knowledge-area',
    KnowledgeAreaViewSet,
    basename='knowledge-area'
)

urlpatterns = router.urls
