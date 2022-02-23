
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp_steps.models import QuestionStepOneAbp, AnswerStepOneAbp
from applications.abp.models import TeamAbp
from .serializers import QuestionsByTeamAbpSerializer
from applications.abp_steps.api.api_answer_step_one_abp.serializers import \
    AnswersAbpByQuestionSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_questions_step_one_count(request, team):
    if request.method == 'GET':
        if team:
            questions_count = QuestionStepOneAbp.objects.get_questions_count_by_team_abp(team)
            if questions_count is not None:
                return Response(
                    {
                        'ok': True,
                        'conon_data': questions_count
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el estudiante enviado.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los valores necesarios para la consulta.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])
@permission_classes([IsStudent])
def get_questions_and_answers_step_by_team(request, team):
    if request.method == 'GET':
        if team:
            questions = TeamAbp.objects.\
                get_questions_step_one_by_team(team)
            if questions is not None:
                questions_and_answers = []
                questions_serializer = QuestionsByTeamAbpSerializer(
                    questions,
                    many=True
                )
                for question in questions_serializer.data:
                    answer = AnswerStepOneAbp.objects.\
                        get_answers_step_one_by_question(question['id'])
                    if answer is not None:
                        answer_serializer = AnswersAbpByQuestionSerializer(answer, many=True)
                        questions_and_answers.append({
                            'question': question,
                            'answer': answer_serializer.data
                        })
                    else:
                        questions_and_answers.append({
                            'question': question,
                            'answer': []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': questions_and_answers
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar los datos necesarios.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los valores necesarios para la consulta.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
