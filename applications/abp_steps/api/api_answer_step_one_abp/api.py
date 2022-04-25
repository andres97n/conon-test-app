
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsTeacher
from applications.abp_steps.models import QuestionStepOneAbp
from .serializers import AnswerAbpByQuestionStepOneAbpSerializer


@api_view(['GET'])
@permission_classes([IsTeacher])
def get_answer_by_team(request, team):
    if request.method == 'GET':
        if team:
            answer_abp = QuestionStepOneAbp.objects.get_answers_by_team(team=team)
            if answer_abp is not None:
                answer_abp_serializer = AnswerAbpByQuestionStepOneAbpSerializer(
                    answer_abp, many=True
                )
                return Response(
                    {
                        'ok': True,
                        'conon_data': answer_abp_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró ninguna respuesta, por favor revise el grupo.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envió el estudiante.'
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
