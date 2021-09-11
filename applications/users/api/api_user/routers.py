from rest_framework.routers import DefaultRouter

from applications.users.api.api_user.api import user_api_view, user_detail_api_view

router = DefaultRouter()

router.register(
    r'user',
    user_api_view,
    basename='user_view'
)
router.register(
    r'user/<int:pk>',
    user_detail_api_view,
    basename='user_detail_view'
)

urlpatterns = router.urls
