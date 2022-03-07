
from django.urls import path

from .api.api_opinion_step_one_abp.api import (get_opinions_by_team_detail,
                                               get_opinions_and_interactions_by_team_and_user,
                                               get_opinions_step_one_count,
                                               get_team_opinions_and_interactions)
from .api.api_question_step_one_abp.api import get_questions_step_one_count, \
    get_questions_and_answers_step_by_team
from .api.api_student_idea_step_two_abp.api import (get_student_ideas_by_team_detail,
                                                    get_student_ideas_and_rates_by_team_and_user,
                                                    get_ideas_and_rates_by_team)
from .api.api_learned_concept_step_three_abp.api import get_learned_concepts_with_references
from .api.api_unknown_concept_step_four_abp.api import get_unknown_concepts_with_references
from .api.api_perform_action_step_five_abp.api import (get_student_actions_by_team_detail,
                                                       get_student_actions_and_rates_by_team_and_user,
                                                       get_student_actions_and_rates_by_team)
from .api.api_problem_definition_step_six_abp.api import get_problem_definition_with_references
from .api.api_get_information_step_seven_abp.api import get_information_model_with_references

urlpatterns = [
    path(
        r"step-one/opinion/user-opinions/<int:team_detail>/",
        get_opinions_by_team_detail,
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
        r"step-one/opinion/team-opinions-interactions/<int:team>/",
        get_team_opinions_and_interactions,
        name="team_opinions_and_interactions_step_one"
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
    path(
        r"step-two/student-idea/team-detail/<int:team_detail>/",
        get_student_ideas_by_team_detail,
        name="student_ideas_by_team_detail"
    ),
    path(
        r"step-two/student-idea/team-student-ideas-rates/<int:team>/<int:user>/",
        get_student_ideas_and_rates_by_team_and_user,
        name="student_ideas_and_rates_by_team"
    ),
    path(
        r"step-two/student-idea/team-ideas-rates/<int:team>/",
        get_ideas_and_rates_by_team,
        name="team_ideas_and_rates_step_two"
    ),
    path(
        r"step-three/learned-concept/learned-concepts-references/<int:team>/",
        get_learned_concepts_with_references,
        name="learned_concepts_and_references_by_team"
    ),
    path(
        r"step-four/unknown-concept/unknown-concepts-references/<int:team>/",
        get_unknown_concepts_with_references,
        name="unknown_concepts_and_references_by_team"
    ),
    path(
        r"step-five/perform-action/student-perform-actions/<int:team_detail>/",
        get_student_actions_by_team_detail,
        name="student_perform_actions_by_team_detail"
    ),
    path(
        r"step-five/perform-action/team-perform-actions-rates-user/<int:team>/<int:user>/",
        get_student_actions_and_rates_by_team_and_user,
        name="perform_actions_and_rates_by_team_exclude_user"
    ),
    path(
        r"step-five/perform-action/team-perform-actions-rates/<int:team>/",
        get_student_actions_and_rates_by_team,
        name="perform_actions_and_rates_by_team"
    ),
    path(
        r"step-six/problem-definition/team-definition-references/<int:team>/",
        get_problem_definition_with_references,
        name="problem_definition_and_references"
    ),
    path(
        r"step-seven/get-information-abp/get-information-abp-reference/<int:team>/",
        get_information_model_with_references,
        name="get_information_abp_and_references"
    ),
]
