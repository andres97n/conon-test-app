from rest_framework import routers

from .api.api_topic.viewsets import TopicViewSet
from .api.api_comment.viewsets import CommentViewSet
from .api.api_reply.viewsets import ReplyViewSet
from .api.api_topic_student_evaluation.viewsets import TopicStudentEvaluationViewSet

router = routers.DefaultRouter()

router.register(
    r'topic',
    TopicViewSet,
    basename='topic'
)
router.register(
    r'comment',
    CommentViewSet,
    basename='comment'
)
router.register(
    r'reply',
    ReplyViewSet,
    basename='reply'
)
router.register(
    r'topic-student-evaluation',
    TopicStudentEvaluationViewSet,
    basename='topic_student_evaluation'
)

urlpatterns = router.urls
