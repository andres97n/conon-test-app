

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.ac_roles.models import SpokesmanQuestionAc, TeacherAnswerAc
from .serializers import SpokesmanQuestionAcListSerializer
from applications.ac_roles.api.api_teacher_answer_ac.serializers import TeacherAnswerAcListSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_questions_and_answers_ac(request, team_detail):
    if request.method == 'GET':
        if team_detail:
            questions_ac = SpokesmanQuestionAc.objects.get_questions_by_team_detail(team_detail=team_detail)
            if questions_ac is not None:
                questions_and_answers = []
                questions_serializer = SpokesmanQuestionAcListSerializer(
                    questions_ac,
                    many=True
                )
                for question in questions_serializer.data:
                    answer = TeacherAnswerAc.objects.\
                        get_answer_by_question(question=question['id'])
                    if answer is not None:
                        answer_serializer = TeacherAnswerAcListSerializer(answer)
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
                        'detail': 'No se pudo encontrar el integrante del equipo, por favor revise.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el integrante para la consulta.'
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