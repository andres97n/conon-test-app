from rest_framework.routers import DefaultRouter

from applications.users.api.api_user.viewsets import UserViewSet
from applications.users.api.api_person.viewsets import PersonViewSet
from applications.users.api.api_student.viewsets import StudentViewSet
from applications.users.api.api_teacher.viewsets import TeacherViewSet
from applications.users.api.api_conversation.viewsets import ConversationViewSet
from applications.users.api.api_conversation_detail.viewsets import ConversationDetailViewSet

router = DefaultRouter()

router.register(
    r'users',
    UserViewSet,
    basename='users'
)
router.register(
    r'person',
    PersonViewSet,
    basename='person'
)
router.register(
    r'student',
    StudentViewSet,
    basename='student'
)
router.register(
    r'teacher',
    TeacherViewSet,
    basename='teacher'
)
router.register(
    r'conversation',
    ConversationViewSet,
    basename='conversation'
)
router.register(
    r'conversation-detail',
    ConversationDetailViewSet,
    basename='conversation_detail'
)

urlpatterns = router.urls
