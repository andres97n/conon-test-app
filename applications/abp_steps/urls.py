
from django.urls import path

from .api.api_opinion_step_one_abp.api import get_opinions_by_team_and_user, \
    get_opinions_and_interactions_by_team_and_user


urlpatterns = [
    path(
        r"step-one/opinion/user-opinions/<int:team>/<int:user>/",
        get_opinions_by_team_and_user,
        name="user_opinions_step_one"
    ),
    path(
        r"step-one/opinion/user-opinions-interactions/<int:team>/<int:user>/",
        get_opinions_and_interactions_by_team_and_user,
        name="user_opinions_and_interactions_step_one"
    ),
]
