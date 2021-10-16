from rest_framework import routers

from .api.api_topic.viewsets import TopicViewSet
from .api.api_comment.viewsets import CommentViewSet
from .api.api_reply.viewsets import ReplyViewSet

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

urlpatterns = router.urls
