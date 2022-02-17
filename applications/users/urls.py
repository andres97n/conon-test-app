from django.urls import path

from applications.users.api.api_student.api import get_student_by_user

urlpatterns = [
    path(
        r"student/user/<int:user>/",
        get_student_by_user,
        name="student_by_user"
    ),
]
