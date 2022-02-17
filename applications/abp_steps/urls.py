
from django.urls import path

from .api.api_opinion_step_one_abp.api import get_opinions_by_team, \
    get_opinions_and_interactions_by_team_and_user, get_opinions_step_one_count
from .api.api_question_step_one_abp.api import get_questions_step_one_count, \
    get_questions_and_answers_step_by_team


urlpatterns = [
    path(
        r"step-one/opinion/user-opinions/<int:team>/",
        get_opinions_by_team,
        name="user_opinions_step_one"
    ),
    path(
        r"step-one/opinion/user-opinions-interactions/<int:team>/<int:user>/",
        get_opinions_and_interactions_by_team_and_user,
        name="user_opinions_and_interactions_step_one"
    ),
    path(
        r"step-one/opinion/user-opinions-count/<int:team>/",
        get_opinions_step_one_count,
        name="user_opinions_step_one_count"
    ),
    path(
        r"step-one/question/moderator-questions-count/<int:team>/",
        get_questions_step_one_count,
        name="moderator_questions_step_one_count"
    ),
    path(
        r"step-one/question/questions-and-answers/<int:team>/",
        get_questions_and_answers_step_by_team,
        name="questions_and_answers_step_one_abp"
    ),
]
