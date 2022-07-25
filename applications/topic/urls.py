from django.urls import path

from applications.topic.api.api_topic.api import (get_topics_list_by_student,
                                                  get_current_topics_list_by_student,
                                                  get_new_students_for_topic,
                                                  get_students_by_topic,
                                                  get_inactive_topics_list_by_student)

urlpatterns = [
    path(
        r"topic/topics-by-student/<int:user>/",
        get_topics_list_by_student,
        name="topics_by_student"
    ),
    path(
        r"topic/current-topics-by-student/<int:user>/",
        get_current_topics_list_by_student,
        name="current_topics_by_student"
    ),
    path(
        r"topic/new-students/<int:topic>/<int:classroom>/",
        get_new_students_for_topic,
        name="topics_new_students"
    ),
    path(
        r"topic/students-by-topic/<int:topic>/",
        get_students_by_topic,
        name="students_by_topic"
    ),
    path(
        r"topic/inactive-topic/<int:user>/<int:school_period>/",
        get_inactive_topics_list_by_student,
        name="inactive_student_topic"
    )
]
