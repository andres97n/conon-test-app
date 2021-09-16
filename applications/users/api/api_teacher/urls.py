from django.urls import path

from applications.users.api.api_teacher.api import teacher_api_view, teacher_detail_api_view

urlpatterns = [
    path(
        'teacher/',
        teacher_api_view,
        name='teacher_view',
    ),
    path(
        'teacher/<int:pk>/',
        teacher_detail_api_view,
        name='teacher_detail_view',
    ),
]
