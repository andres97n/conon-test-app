from django.urls import path

from .api.api_knowledge_area.api import get_teachers_by_knowledge_area
from .api.api_classroom.api import get_classrooms_list_by_teacher, get_classroom_by_student
from .api.api_glossary.api import get_glossary_with_detail


urlpatterns = [
    path(
        r"knowledge-area/teachers/<int:area>/",
        get_teachers_by_knowledge_area,
        name="area_teachers"
    ),
    path(
        r"classroom/teacher/<int:user>/",
        get_classrooms_list_by_teacher,
        name="classroom_teacher"
    ),
    path(
        r"classroom/student/<int:user>/",
        get_classroom_by_student,
        name="classroom_student"
    ),
    path(
        r"glossary/detail/<int:classroom>/<int:active>/",
        get_glossary_with_detail,
        name="glossary_with_details"
    ),
]
