from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import AbpSerializer
from applications.base.permissions import IsOwnerAndTeacher
from applications.base.paginations import CononPagination


class AbpViewSet(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = AbpSerializer
    permission_classes = [IsOwnerAndTeacher]
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Return ABP Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_abp_list()
        return self.get_serializer().Meta.model.objects.get_abp_by_id(pk)

    # Get ABP List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        abp_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create ABP
    def create(self, request, *args, **kwargs):
        abp_serializer = self.get_serializer(data=request.data)
        if abp_serializer.is_valid():
            abp_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Tema de Estudio creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update ABP
    def update(self, request, pk=None, *args, **kwargs):
        abp = self.get_queryset(pk)
        if abp:
            # Send information to serializer referencing the instance
            abp_serializer = self.get_serializer(abp, data=request.data)
            if abp_serializer.is_valid():
                abp_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail ABP
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            abp_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        abp = self.get_queryset(pk)
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

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
