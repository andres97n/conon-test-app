from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import StudentSerializer
from applications.base.permissions import IsTeacher
from applications.base.paginations import CononPagination

# TODO: Crear un método que elimine de la base de datos la información de person,
#   student y user si es que los métodos de guardar y eliminar fallan
#       (Utilizar verifySaveTeacher en Frontend).


class StudentViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsTeacher])
    pagination_class = CononPagination
    serializer_class = StudentSerializer
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Return Student data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_student_list()
        return self.get_serializer().Meta.model.objects.get_student_detail_data(pk)

    # Get Student List
    def list(self, request, *args, **kwargs):
        student_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(student_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        student_serializer = self.get_serializer(student_queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': student_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Student data
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        student_serializer = self.serializer_class(data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': student_serializer.data['id'],
                    'message': 'Estudiante creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': student_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Student data
    def update(self, request, pk=None, *args, **kwargs):
        student = self.get_queryset(pk)
        if student:
            # Send information to serializer referencing the instance
            student_serializer = self.serializer_class(student, data=request.data)
            if student_serializer.is_valid():
                student_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': student_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': student_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Estudiante.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Student Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            student_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': student_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Estudiante.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Student
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        student = self.get_queryset(pk)
        if student:
            student.auth_state = 'I'
            student.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Estudiante eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Estudiante.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Many Students
    @action(detail=False, methods=(['DELETE']), url_path='destroy-students')
    def destroy_students(self, request):
        students = self.get_serializer().Meta.model.objects.get_many_students(request.data['students'])
        if students:
            for student in students:
                student.auth_state = 'I'

            self.get_serializer().Meta.model.objects.bulk_update(students, ['auth_state'])

            return Response(
                {
                    'ok': True,
                    'message': 'Estudiantes eliminados correctamente.'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se puede eliminar a estos Estudiantes.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
