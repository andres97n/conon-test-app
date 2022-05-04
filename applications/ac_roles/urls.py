from django.urls import path

from .api.api_spokesman_question_ac.api import get_questions_and_answers_ac

urlpatterns = [
    path(
        r"spokesman-question-ac/questions-and-answers-ac/<int:team_detail>/",
        get_questions_and_answers_ac,
        name="questions_and_answers_ac"
    ),
]
