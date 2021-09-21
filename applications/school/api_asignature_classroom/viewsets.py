from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .serializers import AsignatureClassroomSerializer
from applications.base.paginations import CononPagination


class AsignatureClassroomViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = AsignatureClassroomSerializer
    pagination_class = CononPagination

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_asignature_classroom_list()
        return self.get_serializer().Meta.model.objects.get_asignature_classroom_by_id(pk)

    # Create Asignature Classroom Data
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        asignature_classroom_serializer = self.serializer_class(data=request.data)
        if asignature_classroom_serializer.is_valid():
            asignature_classroom_serializer.save()

            return Response(
                {
                    'message': 'Valores creados correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            asignature_classroom_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Asignature Classroom Data
    def update(self, request, pk=None, *args, **kwargs):
        asignature_classroom = self.get_queryset(pk)
        if asignature_classroom:
            # Send information to serializer referencing the instance
            asignature_classroom_serializer = self.serializer_class(asignature_classroom, data=request.data)
            if asignature_classroom_serializer.is_valid():
                asignature_classroom_serializer.save()

                return Response(
                    asignature_classroom_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                asignature_classroom_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'error': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Asignature Classroom Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            asignature_classroom_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                asignature_classroom_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Registro.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Asignature Classroom Data
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        asignature_classroom = self.get_queryset(pk)
        if asignature_classroom:
            asignature_classroom.auth_state = 'I'
            asignature_classroom.save()

            return Response(
                {
                    'message': 'Registro eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Registro.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
