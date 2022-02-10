from django.urls import path

from applications.topic.api.api_topic.api import get_topics_list_by_student

urlpatterns = [
    path(
        r"topic/topics-by-student/<int:user>/",
        get_topics_list_by_student,
        name="topics_by_student"
    )
]
