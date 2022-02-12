
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.users.models import Student
from applications.users.api.api_student.serializers import StudentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_by_user(request, user):
    if request.method == 'GET':
        if user:
            student = Student.objects.get_student_by_user_object(user)
            if student:
                student_serializer = StudentSerializer(student)
                return Response(
                    {
                        'ok': True,
                        'detail': student_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontro el Estudiante.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Usuario.'
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

