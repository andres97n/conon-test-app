
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import SecretaryInformationAcSerializer, SecretaryInformationAcListSerializer
from applications.ac.models import TeamDetailAc


class SecretaryInformationAcViewSet(viewsets.GenericViewSet):
    serializer_class = SecretaryInformationAcSerializer
    list_serializer_class = SecretaryInformationAcListSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_ac', 'active']

# Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_secretary_information_ac_active_queryset(),
            id=pk
        )

    # Return Secretary Information Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_secretary_information_ac_list()

    # Get Secretary Information Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        secretary_information_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': secretary_information_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Secretary Information Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        secretary_information_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if secretary_information_ac_serializer.is_valid():
            secretary_information_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'secretary_information_ac':
                        secretary_information_ac_serializer.data
                        if isinstance(secretary_information_ac_serializer.data, list)
                        else secretary_information_ac_serializer.data['id'],
                    'message':
                        'Enlaces agregados correctamente'
                        if isinstance(secretary_information_ac_serializer.data, list)
                        else 'Enlace agregado correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': secretary_information_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Secretary Information Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_secretary_information_ac(self, request, pk=None):
        secretary_information_ac = self.get_object(pk)
        secretary_information_ac.active = False
        secretary_information_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Enlace bloqueado correctamente.'
            },
            status=status.HTTP_200_OK
        )

    # Get Secretary Information By Team Detail Ac
    @action(detail=True, methods=['GET'], url_path='by-team-detail')
    def get_secretary_information_by_team_detail_ac(self, request, pk=None):
        team_detail_ac = TeamDetailAc.objects.get_team_ac_active_object_queryset(pk=pk)
        if team_detail_ac is not None:
            secretary_information = self.serializer_class().Meta.model.objects. \
                get_secretary_information_by_team(team_ac=team_detail_ac.team_ac)
            if secretary_information is not None:
                secretary_information_serializer = self.list_serializer_class(
                    secretary_information, many=True
                )

                return Response(
                    {
                        'ok': True,
                        'conon_data': secretary_information_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar enlaces del equipo.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se pudo encontrar el integrante.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
