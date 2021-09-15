from rest_framework.decorators import api_view, permission_classes

from applications.users.models import Student
from .serializers import StudentSerializer, StudentListSerializer
from applications.users.paginations import CononPagination


# TODO: Revisar los permisos para la administración
#   de datos del estudiante

# Get all active Student records
# Create a Student
@api_view(['GET', 'POST'])
def student_api_view(request):
    # Student List
    if request.method == 'GET':
        paginator = CononPagination()
        students = Student.objects.filter(auth_state='A')
        context = paginator.paginate_queryset(students, request)
        student_serializer = StudentListSerializer(context, many=True)

        return paginator.get_paginated_response(student_serializer.data)

    # Create Student
    elif request.method == 'POST':
        student_serializer = StudentSerializer(data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response(
                {
                    'message': 'Estudiante creado correctamente!!'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            student_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        return Response(
            {
                'error': 'Método no permitido'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET', 'PUT', 'DELETE'])
def student_detail_api_view(request, pk=None):

    # Get Student
    student = Student.objects.filter(id=pk).first()
    if student:

        # Student Detail
        if request.method == 'GET':
            student_serializer = StudentListSerializer(student)

            return Response(
                student_serializer.data,
                status=status.HTTP_200_OK
            )

        # Update Student
        elif request.method == 'PUT':
            student_serializer = StudentSerializer(student, data=request.data)
            if student_serializer.is_valid():
                student_serializer.save()

                return Response(
                    student_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                student_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Delete Student
        elif request.method == 'DELETE':
            student.auth_state = 'I'
            student.save()

            return Response(
                {
                    'message': 'Estudiante eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'Método no permitido'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    return Response(
        {
            'error': 'No existe este Estudiante.'
        },
        status=status.HTTP_400_BAD_REQUEST
    )
