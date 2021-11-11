from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import AsignatureSerializer
from applications.base.paginations import CononPagination


class AsignatureViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = AsignatureSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_asignature_list()
        return self.get_serializer().Meta.model.objects.get_asignature_by_id(pk)

    # Get Classroom List
    def list(self, request, *args, **kwargs):
        asignature_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(asignature_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        asignature_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': asignature_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Asignature
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        asignature_serializer = self.get_serializer(data=request.data)
        if asignature_serializer.is_valid():
            asignature_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': asignature_serializer.data['id'],
                    'message': 'Asignatura creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': asignature_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Asignature
    def update(self, request, pk=None, *args, **kwargs):
        asignature = self.get_queryset(pk)
        if asignature:
            # Send information to serializer referencing the instance
            asignature_serializer = self.get_serializer(asignature, data=request.data)
            if asignature_serializer.is_valid():
                asignature_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': asignature_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': asignature_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Asignature Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            asignature_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': asignature_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Asignatura.'
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
                    'ok': True,
                    'message': 'Asignatura eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Asignatura.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
