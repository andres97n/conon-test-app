from django.urls import path

from applications.users.api.api_student.api import student_api_view, student_detail_api_view

urlpatterns = [
    path(
        'student/',
        student_api_view,
        name='student_view',
    ),
    path(
        'student/<int:pk>/',
        student_detail_api_view,
        name='student_detail_view',
    ),
]
