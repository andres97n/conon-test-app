from django.urls import path

from applications.dua.api.api_activity.api import get_activity_with_questions
from applications.dua.api.api_activity_student.api import get_student_activity_with_details
from applications.dua.api.api_activity_student.api import get_is_student_activity_exists
from applications.dua.api.api_dua.api import get_student_evaluation_by_topic


urlpatterns = [
    path(
        r"activity/activity-questions/<int:dua>/",
        get_activity_with_questions,
        name="activity_with_questions"
    ),
    path(
        r"activity-student/activity-student-answers/<int:activity>/<int:owner>/",
        get_student_activity_with_details,
        name="activity_student_with_answers"
    ),
    path(
        r"activity-student/activity-students-exists/<int:activity>/<int:owner>/",
        get_is_student_activity_exists,
        name="activity_student_exists"
    ),
    path(
        r"dua/student-evaluation/<int:topic>/<int:user>/",
        get_student_evaluation_by_topic,
        name="student_evaluation_by_topic"
    ),
]
