from django.urls import path

from applications.topic.api.api_topic.api import (get_topics_list_by_student,
                                                  get_new_students_for_topic)

urlpatterns = [
    path(
        r"topic/topics-by-student/<int:user>/",
        get_topics_list_by_student,
        name="topics_by_student"
    ),
    path(
        r"topic/new-students/<int:topic>/<int:classroom>/",
        get_new_students_for_topic,
        name="topics_new_students"
    )
]
