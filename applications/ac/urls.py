from django.urls import path

from applications.ac.api.api_team_ac.api import (get_student_team_abc, get_team_detail_ac_by_user,
                                                 get_team_ac_with_students, is_team_ac_finished,
                                                 get_team_secretary_ac_by_ac, new_team_detail_ac)
from applications.ac.api.api_rubric_ac.api import get_rubric_abp_detail_list_by_abp
from applications.ac.api.api_student_evaluation_ac.api import (get_evaluation_ac_with_details,
                                                               get_student_evaluation_ac_with_details)
from applications.ac.api.api_ac.api import get_student_evaluation_ac_by_topic

urlpatterns = [
    path(
        r"team-ac/student-team-ac/<int:ac>/<int:user>/",
        get_student_team_abc,
        name="student_team_ac"
    ),
    path(
        r"rubric-ac/current-rubric-ac/<int:ac>/",
        get_rubric_abp_detail_list_by_abp,
        name="current_rubric_ac"
    ),
    path(
        r"team-detail-ac/user-ac/<int:ac>/<int:user>/",
        get_team_detail_ac_by_user,
        name="team_detail_ac_by_user_and_ac"
    ),
    path(
        r"team-ac/team-ac-with-students/<int:ac>/",
        get_team_ac_with_students,
        name="team_ac_with_students"
    ),
    path(
        r"student-evaluation-ac/current-student-evaluation-ac/<int:rubric>/<int:team_detail_ac>/",
        get_evaluation_ac_with_details,
        name="current_student_evaluation_ac"
    ),
    path(
        r"student-evaluation-ac/current-student-evaluation-by-ac/<int:ac>/<int:team_detail_ac>/",
        get_student_evaluation_ac_with_details,
        name="current_student_evaluation_by_ac"
    ),
    path(
        r"team-ac/team-ac-finished/<int:team>/",
        is_team_ac_finished,
        name="is_team_ac_finished"
    ),
    path(
        r"ac/student-evaluation-ac/<int:topic>/<int:user>/",
        get_student_evaluation_ac_by_topic,
        name="student_evaluation_ac"
    ),
    path(
        r"team-detail-ac/secretary-team/<int:ac>/",
        get_team_secretary_ac_by_ac,
        name="team_secretary_ac"
    ),
    path(
        r"team-detail-ac/new/",
        new_team_detail_ac,
        name="new_team_detail_ac"
    ),
]
