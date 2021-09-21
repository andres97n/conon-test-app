from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .serializers import StudentSerializer, StudentListSerializer
from applications.base.paginations import CononPagination


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    pagination_class = CononPagination
    serializer_class = StudentSerializer

    # Return Student data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_student_list()
        return self.get_serializer().Meta.model.objects.get_person_data(pk)

    # Create Student data
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        student_serializer = self.serializer_class(data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()

            return Response(
                {
                    'message': 'Estudiante creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            student_serializer.errors,
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
                    student_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                student_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'error': 'No existe este Estudiante.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Student data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            student_serializer = StudentListSerializer(self.get_queryset(pk))

            return Response(
                student_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Estudiante.'
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
                    'message': 'Estudiante eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Estudiante.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
