
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.dua.models import Dua, ActivityStudent
from applications.dua.api.api_activity_student.serializers import ActivityStudentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_evaluation_by_topic(request, topic, user):
    if request.method == 'GET':
        if topic and user:
            dua = Dua.objects.get_dua_by_topic(pk=topic)
            if dua is not None:
                activity_student = ActivityStudent.objects.get_activity_student_by_dua(
                    dua=dua.id, owner=user
                )
                if activity_student is not None:
                    current_activity = {}
                    if activity_student:
                        activity_student_serializer = ActivityStudentSerializer(activity_student)
                        current_activity = activity_student_serializer.data
                    return Response(
                        {
                            'ok': True,
                            'conon_data': current_activity
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontró la Actividad del Estudiante.'
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
