from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from applications.base.paginations import CononPagination
from .serializers import TeacherSerializer, TeacherListSerializer


# TODO: Revisar los permisos para esta clase y
#   la clase Student


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    pagination_class = CononPagination
    serializer_class = TeacherSerializer

    # Return teacher data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_teacher_list()
        return self.get_serializer().Meta.model.objects.get_person_data(pk)

    # Create Teacher
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        teacher_serializer = self.serializer_class(data=request.data)
        if teacher_serializer.is_valid():
            teacher_serializer.save()

            return Response(
                {
                    'message': 'Docente creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            teacher_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Teacher
    def update(self, request, pk=None, *args, **kwargs):
        teacher = self.get_queryset(pk)
        if teacher:
            # Send information to serializer referencing the instance
            teacher_serializer = self.serializer_class(teacher, data=request.data)
            if teacher_serializer.is_valid():
                teacher_serializer.save()

                return Response(
                    teacher_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                teacher_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'error': 'No existe este Docente.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Teacher data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            teacher_serializer = TeacherListSerializer(self.get_queryset(pk))

            return Response(
                teacher_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Docente.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Teacher
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        teacher = self.get_queryset(pk)
        if teacher:
            teacher.auth_state = 'I'
            teacher.save()

            return Response(
                {
                    'message': 'Docente eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Docente.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
