from rest_framework.routers import DefaultRouter

from applications.users.api.api_user.viewsets import UserViewSet
from applications.users.api.api_person.viewsets import PersonViewSet
from applications.users.api.api_student.viewsets import StudentViewSet
from applications.users.api.api_teacher.viewsets import TeacherViewSet

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

urlpatterns = router.urls
