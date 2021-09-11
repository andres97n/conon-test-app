from django.urls import path

from applications.users.api.api_user.api import user_api_view, user_detail_api_view

urlpatterns = [
    path(
        'user/',
        user_api_view,
        name='user_view',
    ),
    path(
        'user/<int:pk>/',
        user_detail_api_view,
        name='user_detail_view',
    ),
]
