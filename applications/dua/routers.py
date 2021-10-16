from rest_framework import routers

from .api.api_dua.viewsets import DuaViewSet
from .api.api_activity.viewsets import ActivityViewSet
from .api.api_question.viewsets import QuestionViewSet
from .api.api_activity_student.viewsets import ActivityStudentViewSet
from .api.api_answer.viewsets import AnswerViewSet

router = routers.DefaultRouter()

router.register(
    r'dua',
    DuaViewSet,
    basename='dua'
)
router.register(
    r'activity',
    ActivityViewSet,
    basename='activity'
)
router.register(
    r'question',
    QuestionViewSet,
    basename='question'
)
router.register(
    r'activity-student',
    ActivityStudentViewSet,
    basename='activity_student'
)
router.register(
    r'answer',
    AnswerViewSet,
    basename='answer'
)

urlpatterns = router.urls
