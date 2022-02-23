from rest_framework import routers

from .api.api_opinion_step_one_abp.viewsets import OpinionStepOneAbpViewSet
from .api.api_interaction_step_one_abp.viewsets import InteractionStepOneAbpViewSet
from .api.api_question_step_one_abp.viewsets import QuestionStepOneAbpViewSet
from .api.api_answer_step_one_abp.viewsets import AnswerStepOneAbpViewSet
from .api.api_student_idea_step_two_abp.viewsets import StudentIdeaStepTwoAbpViewSet
from .api.api_rate_student_idea_step_two_abp.viewsets import RateStudentIdeaStepTwoAbpViewSet
from .api.api_learned_concept_step_three_abp.viewsets import LearnedConceptStepThreeAbpViewSet
from .api.api_learned_concept_reference_step_three_abp.viewsets import \
    LearnedConceptReferenceStepThreeAbpViewSet

router = routers.DefaultRouter()

router.register(
    r'step-one/opinion',
    OpinionStepOneAbpViewSet,
    basename='opinion_step_one_abp'
)
router.register(
    r'step-one/interaction',
    InteractionStepOneAbpViewSet,
    basename='interaction_step_one_abp'
)
router.register(
    r'step-one/question',
    QuestionStepOneAbpViewSet,
    basename='question_step_one_abp'
)
router.register(
    r'step-one/answer',
    AnswerStepOneAbpViewSet,
    basename='answer_step_one_abp'
)
router.register(
    r'step-two/student-idea',
    StudentIdeaStepTwoAbpViewSet,
    basename='student_idea_step_two_abp'
)
router.register(
    r'step-two/rate-student-idea',
    RateStudentIdeaStepTwoAbpViewSet,
    basename='rate_student_idea_step_two_abp'
)
router.register(
    r'step-three/learned-concept',
    LearnedConceptStepThreeAbpViewSet,
    basename='learned_concept_step_three_abp'
)
router.register(
    r'step-three/learned-concept-reference',
    LearnedConceptReferenceStepThreeAbpViewSet,
    basename='learned_concept_reference_step_three_abp'
)

urlpatterns = router.urls
