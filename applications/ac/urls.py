from django.urls import path

from applications.ac.api.api_team_ac.api import get_student_team_abp
from applications.ac.api.api_rubric_ac.api import get_rubric_abp_detail_list_by_abp
from applications.ac.api.api_student_evaluation_ac.api import get_evaluation_apb_with_details

urlpatterns = [
    path(
        r"team-ac/student-team-ac/<int:ac>/<int:user>/",
        get_student_team_abp,
        name="student_team_ac"
    ),
    path(
        r"rubric-ac/current-rubric-ac/<int:ac>/",
        get_rubric_abp_detail_list_by_abp,
        name="current_rubric_ac"
    ),
    path(
        r"student-evaluation-ac/current-student-evaluation-ac/<int:rubric>/<int:team_detail_ac>/",
        get_evaluation_apb_with_details,
        name="current_student_evaluation_ac"
    ),
]
