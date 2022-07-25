

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.abp.models import Abp, EvaluationAbp
from applications.abp.api.api_evaluation_abp.serializers import EvaluationAbpByAbpSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_evaluation_abp_by_topic(request, topic, user):
    if request.method == 'GET':
        if topic and user:
            abp = Abp.objects.get_abp_by_topic(topic=topic)
            if abp is not None:
                evaluation = EvaluationAbp.objects.get_student_evaluation_by_abp_and_user(
                    abp=abp.id, user=user
                )
                if evaluation is not None:
                    current_evaluation = {}
                    if evaluation:
                        evaluation_serializer = EvaluationAbpByAbpSerializer(evaluation)
                        current_evaluation = evaluation_serializer.data
                    return Response(
                        {
                            'ok': True,
                            'conon_data': current_evaluation
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontró la Evaluación.'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el Tema de Estudio.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envio la información necesaria.'
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
