
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import FeaturedInformationSecretaryAcSerializer, FeaturedInformationSecretaryAcListSerializer


class FeaturedInformationSecretaryAcViewSet(viewsets.GenericViewSet):
    serializer_class = FeaturedInformationSecretaryAcSerializer
    list_serializer_class = FeaturedInformationSecretaryAcListSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_ac', 'member_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_featured_information_secretary_ac_active_queryset(),
            id=pk
        )

    # Return Featured Information Secretary Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_featured_information_secretary_ac_list()

    # Get Featured Information Secretary Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        featured_information_secretary_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': featured_information_secretary_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Featured Information Secretary Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        featured_information_secretary_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if featured_information_secretary_ac_serializer.is_valid():
            featured_information_secretary_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'featured_information_ac':
                        featured_information_secretary_ac_serializer.data
                        if isinstance(featured_information_secretary_ac_serializer.data, list)
                        else featured_information_secretary_ac_serializer.data['id'],
                    'message':
                        'Registros agregados correctamente'
                        if isinstance(featured_information_secretary_ac_serializer.data, list)
                        else 'Información agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': featured_information_secretary_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Featured Information Secretary Ac
    def update(self, request, pk=None):
        featured_information_secretary_ac = self.get_object(pk)
        # Send information to serializer referencing the instance
        featured_information_secretary_ac_serializer = self.serializer_class(
            featured_information_secretary_ac, data=request.data
        )
        if featured_information_secretary_ac_serializer.is_valid():
            featured_information_secretary_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'conon_data': featured_information_secretary_ac_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': featured_information_secretary_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Featured Information Secretary Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_featured_information_secretary_ac(self, request, pk=None):
        featured_information_secretary_ac = self.get_object(pk)
        featured_information_secretary_ac.active = False
        featured_information_secretary_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Información bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
