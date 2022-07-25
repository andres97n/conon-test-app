from django.urls import path

from applications.abp.api.api_team_abp.api import \
    get_students_by_classroom_for_to_group, get_student_team_abp, get_team_abp_with_students
from applications.abp.api.api_rubric_abp.api import (get_rubric_abp_detail_list_by_abp,
                                                     get_rubric_abp_with_detail_by_abp)
from applications.abp.api.api_evaluation_abp.api import get_evaluation_apb_with_details
from applications.abp.api.api_abp.api import get_student_evaluation_abp_by_topic

urlpatterns = [
    path(
        r"team-abp/new-students-for-team-abp/<int:classroom>/<int:abp>/",
        get_students_by_classroom_for_to_group,
        name="new_students_for_team_abp"
    ),
    path(
        r"team-abp/student-team-abp/<int:abp>/<int:user>/",
        get_student_team_abp,
        name="student_team_abp"
    ),
    path(
        r"rubric-abp/rubric-abp-detail-by-abp/<int:abp>/",
        get_rubric_abp_detail_list_by_abp,
        name="rubric_abp_detail_by_abp"
    ),
    path(
        r"rubric-abp/rubric-abp-with-detail/<int:abp>/",
        get_rubric_abp_with_detail_by_abp,
        name="rubric_abp_with_detail"
    ),
    path(
        r"evaluation-abp/evaluation-abp-detail-by-evaluation/<int:abp>/<int:team_detail_abp>/",
        get_evaluation_apb_with_details,
        name="evaluation_abp_detail_by_evaluation"
    ),
    path(
        r"team-abp/team-abp-with-students/<int:abp>/",
        get_team_abp_with_students,
        name="team_abp_with_students"
    ),
    path(
        r"abp/student-evaluation-abp/<int:topic>/<int:user>/",
        get_student_evaluation_abp_by_topic,
        name="student_evaluation_abp"
    ),
]
