from django.urls import path

from .api.api_student.api import get_topics_list_by_student

urlpatterns = [
    path(
        r"topics-by-student/<int:user>/",
        get_topics_list_by_student,
        name="topics_by_student"
    )
]
