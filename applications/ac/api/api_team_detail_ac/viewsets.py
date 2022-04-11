
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TeamDetailAcSerializer, TeamDetailAcListSerializer
from applications.base.permissions import IsTeacher
from applications.base.paginations import CononPagination


class TeamDetailAcViewSet(viewsets.GenericViewSet):
    serializer_class = TeamDetailAcSerializer
    list_serializer_class = TeamDetailAcListSerializer
    permission_classes = [IsTeacher]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_team_ac_active_queryset(), id=pk
        )

    # Return Team Ac Detail List
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_team_detail_ac_list()

    # Get Team Detail AC List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        team_detail_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': team_detail_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Team Detail Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        team_detail_ac_serializer = self.get_serializer(data=request.data, many=is_many)
        if team_detail_ac_serializer.is_valid():
            team_detail_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'team_detail_ac':
                        team_detail_ac_serializer.data
                        if isinstance(team_detail_ac_serializer.data, list)
                        else team_detail_ac_serializer.data['id'],
                    'message':
                        'Estudiantes agregados correctamente'
                        if isinstance(team_detail_ac_serializer.data, list)
                        else 'Estudiante agregado correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': team_detail_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Team Detail AC
    def update(self, request, pk=None, *args, **kwargs):
        team_detail_abp = self.get_object(pk)
        # Send information to serializer referencing the instance
        team_detail_abp_serializer = self.get_serializer(team_detail_abp, data=request.data)
        if team_detail_abp_serializer.is_valid():
            team_detail_abp_serializer.save()

            return Response(
                {
                    'ok': True,
                    'conon_data': team_detail_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': team_detail_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Team Detail Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_team_detail_ac(self, request, pk=None):
        team_detail_ac = self.get_object(pk)
        team_detail_ac.active = False
        team_detail_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Estudiante bloqueado correctamente.'
            },
            status=status.HTTP_200_OK
        )
