from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TeamAcSerializer, TeamAcListSerializer
from applications.base.permissions import IsTeacher
from applications.base.paginations import CononPagination


class TeamAcViewSet(LoggingMixin, viewsets.GenericViewSet):
    serializer_class = TeamAcSerializer
    list_serializer_class = TeamAcListSerializer
    permission_classes = [IsTeacher]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_ac_active_queryset(), id=pk
        )

    # Return Detail Ac List
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_ac_list()

    # Get Team AC List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        team_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': team_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Team Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        team_ac_serializer = self.get_serializer(data=request.data)
        if team_ac_serializer.is_valid():
            team_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': team_ac_serializer.data['id'],
                    'message': 'Grupo creado correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': team_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Team Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_team_ac(self, request, pk=None):
        team_ac = self.get_object(pk)
        team_ac.active = False
        team_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Grupo bloqueado correctamente.'
            },
            status=status.HTTP_200_OK
        )
