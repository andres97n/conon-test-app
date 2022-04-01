
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import AcSerializer
from applications.base.paginations import CononPagination
from applications.base.permissions import IsTeacher


class AcViewSet(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = AcSerializer
    permission_classes = [IsTeacher]
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic', 'state']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_ac_active_queryset(), id=pk
        )

    # Return Ac List
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_ac_list()

    # Get AC List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        ac_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create AC
    def create(self, request, *args, **kwargs):
        ac_serializer = self.get_serializer(data=request.data)
        if ac_serializer.is_valid():
            ac_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': ac_serializer.data['id'],
                    'message': 'Tema de Estudio creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update AC
    def update(self, request, pk=None, *args, **kwargs):
        ac = self.get_object(pk)
        # Send information to serializer referencing the instance
        ac_serializer = self.get_serializer(ac, data=request.data)
        if ac_serializer.is_valid():
            ac_serializer.save()

            return Response(
                {
                    'ok': True,
                    'conon_data': ac_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail AC
    def retrieve(self, request, pk=None, *args, **kwargs):
        ac = self.get_object(pk)
        ac_serializer = self.get_serializer(ac)

        return Response(
            {
                'ok': True,
                'conon_data': ac_serializer.data,
            },
            status=status.HTTP_200_OK
        )

    # Delete AC
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        abp = self.get_object(pk)
        if abp:
            abp.auth_state = 'I'
            abp.state = 0
            abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Tema de Estudio eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

    # Block AC
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_ac(self, request, pk=None):
        ac = self.get_object(pk)
        ac.state = 0
        ac.save()

        return Response(
            {
                'ok': True,
                'message': 'AC bloqueado correctamente.'
            },
            status=status.HTTP_200_OK
        )
