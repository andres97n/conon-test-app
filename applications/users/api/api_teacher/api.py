from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from applications.users.models import Teacher
from .serializers import TeacherSerializer, TeacherListSerializer
from applications.users.paginations import CononPagination


# Get all active Teacher records
# Create a Teacher
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def teacher_api_view(request):
    # Get Teacher List
    if request.method == 'GET':
        paginator = CononPagination()
        teacher = Teacher.objects.select_related('person').filter(auth_state='A').order_by('person__last_name')
        context = paginator.paginate_queryset(teacher, request)
        teacher_serializer = TeacherListSerializer(context, many=True)

        return paginator.get_paginated_response(teacher_serializer.data)

    # Create Teacher
    elif request.method == 'POST':
        teacher_serializer = TeacherSerializer(data=request.data)
        if teacher_serializer.is_valid():
            teacher_serializer.save()

            return Response(
                {
                    'message': 'Docente creado con éxito.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            teacher_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    else:

        return Response(
            {
                'error': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


# Detail, Update and Delete of a Teacher
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def teacher_detail_api_view(request, pk=None):

    # Get detailed Teacher data
    teacher = Teacher.objects.filter(id=pk).first()
    if teacher:

        # Get detailed Teacher list
        if request.method == 'GET':
            teacher_serializer = TeacherListSerializer(teacher)

            return Response(
                teacher_serializer.data,
                status=status.HTTP_200_OK
            )

        # Update Teacher
        elif request.method == 'PUT':
            teacher_serializer = TeacherSerializer(teacher, data=request.data)
            if teacher_serializer.is_valid():
                teacher_serializer.save()

                return Response(
                    {
                        'message': 'Docente actualizado correctamente.'
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                teacher_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Delete Teacher
        elif request.method == 'DELETE':
            teacher.auth_state = 'I'
            teacher.save()

            return Response(
                {
                    'message': 'Docente eliminado correctamente.'
                }
            )

        return Response(
            {
                'error': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    return Response(
        {
            'error': 'No existe este Docente.'
        },
        status=status.HTTP_400_BAD_REQUEST
    )
