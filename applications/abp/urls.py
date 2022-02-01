from django.urls import path

from applications.abp.api.api_team_abp.api import get_students_by_classroom_for_to_group

urlpatterns = [
    path(
        r"new-students-for-team-abp/<int:classroom>/<int:abp>/",
        get_students_by_classroom_for_to_group,
        name="new_students_for_team_abp"
    )
]
