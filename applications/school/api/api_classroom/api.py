from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from applications.users.models import Teacher, Student
from applications.school.models import Classroom
from .serializers import ClassroomSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_classrooms_list_by_teacher(request, user):
    if request.method == 'GET':
        if user:
            teacher = Teacher.objects.get_teacher_by_user(pk=user)
            if teacher is not None:
                classrooms = Classroom.objects. \
                    get_classrooms_by_teacher(pk=teacher['id'])
                if classrooms is not None:
                    classroom_serializer = ClassroomSerializer(classrooms, many=True)
                    return Response(
                        {
                            'ok': True,
                            'conon_data': classroom_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontró el Docente en presentes Aulas.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el usuario requerido.'
                },
                status=status.HTTP_404_NOT_FOUND
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
@permission_classes([IsAuthenticated])
def get_classroom_by_student(request, user):
    if request.method == 'GET':
        if user:
            student = Student.objects.get_student_by_user_object(user=user)
            if student is not None:
                classroom = Classroom.objects.get_classroom_by_student_assigned(
                    student=student
                )
                if classroom is not None and classroom:
                    classroom_serializer = ClassroomSerializer(classroom.first())
                    return Response(
                        {
                            'ok': True,
                            'conon_data': classroom_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se pudo encontrar el aula del usuario enviado.'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar el estudiante.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el usuario requerido.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
