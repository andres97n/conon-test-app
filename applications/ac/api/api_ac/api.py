
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.ac.models import Ac, StudentEvaluationAc
from applications.ac.api.api_student_evaluation_ac.serializers import \
    StudentEvaluationAcShortListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_evaluation_ac_by_topic(request, topic, user):
    if request.method == 'GET':
        if topic and user:
            ac = Ac.objects.get_ac_by_topic(topic=topic)
            if ac is not None:
                student_evaluation = StudentEvaluationAc.objects.\
                    get_student_evaluation_ac_by_ac_and_user(ac=ac, user=user)
                if student_evaluation is not None:
                    current_evaluation = {}
                    if student_evaluation:
                        student_evaluation_serializer = StudentEvaluationAcShortListSerializer(
                            student_evaluation
                        )
                        current_evaluation = student_evaluation_serializer.data
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
                            'detail': 'No se encontró la evaluación del estudiante.'
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