from rest_framework import routers

from .api.api_opinion_step_one_abp.viewsets import OpinionStepOneAbpViewSet
from .api.api_interaction_step_one_abp.viewsets import InteractionStepOneAbpViewSet
from .api.api_question_step_one_abp.viewsets import QuestionStepOneAbpViewSet
from .api.api_answer_step_one_abp.viewsets import AnswerStepOneAbpViewSet

router = routers.DefaultRouter()

router.register(
    r'step-one/opinion',
    OpinionStepOneAbpViewSet,
    basename='opinion-step-one-abp'
)
router.register(
    r'step-one/interaction',
    InteractionStepOneAbpViewSet,
    basename='interaction-step-one-abp'
)
router.register(
    r'step-one/question',
    QuestionStepOneAbpViewSet,
    basename='question-step-one-abp'
)
router.register(
    r'step-one/answer',
    AnswerStepOneAbpViewSet,
    basename='answer-step-one-abp'
)

urlpatterns = router.urls
