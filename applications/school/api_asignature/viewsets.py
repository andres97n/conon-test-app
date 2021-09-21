from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .serializers import AsignatureSerializer


class AsignatureViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = AsignatureSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_asignature_list()
        return self.get_serializer().Meta.model.objects.get_asignature_by_id(pk)

    # Create Asignature
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        asignature_serializer = self.serializer_class(data=request.data)
        if asignature_serializer.is_valid():
            asignature_serializer.save()

            return Response(
                {
                    'message': 'Asignatura creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            asignature_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Asignature
    def update(self, request, pk=None, *args, **kwargs):
        asignature = self.get_queryset(pk)
        if asignature:
            # Send information to serializer referencing the instance
            asignature_serializer = self.serializer_class(asignature, data=request.data)
            if asignature_serializer.is_valid():
                asignature_serializer.save()

                return Response(
                    asignature_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                asignature_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'error': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Asignature Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            asignature_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                asignature_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe esta Asignatura.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Asignature
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        asignature = self.get_queryset(pk)
        if asignature:
            asignature.auth_state = 'I'
            asignature.save()

            return Response(
                {
                    'message': 'Asignatura eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe esta Asignatura.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
