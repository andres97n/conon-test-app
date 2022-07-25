from django.urls import path

from .api.api_spokesman_question_ac.api import get_questions_and_answers_ac
from .api.api_featured_information_secretary_ac.api import get_current_team_featured_information

urlpatterns = [
    path(
        r"spokesman-question-ac/questions-and-answers-ac/<int:team_detail>/",
        get_questions_and_answers_ac,
        name="questions_and_answers_ac"
    ),
    path(
        r"featured-information-secretary/current-team-information/<int:team_detail>/<int:member>/",
        get_current_team_featured_information,
        name="current_team_featured_information"
    ),
]
