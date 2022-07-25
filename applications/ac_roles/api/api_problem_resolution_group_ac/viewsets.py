
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import ProblemResolutionGroupAcSerializer, ProblemResolutionGroupAcListSerializer
from applications.ac.models import TeamDetailAc


class ProblemResolutionGroupAcViewSet(viewsets.GenericViewSet):
    serializer_class = ProblemResolutionGroupAcSerializer
    list_serializer_class = ProblemResolutionGroupAcListSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_problem_resolution_ac_active_queryset(),
            id=pk
        )

    # Return Problem Resolution Group Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_problem_resolution_ac_list()

    # Get Problem Resolution Group Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        problem_resolution_group_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': problem_resolution_group_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Problem Resolution Group Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        problem_resolution_group_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if problem_resolution_group_ac_serializer.is_valid():
            problem_resolution_group_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'problem_resolution_group_ac':
                        problem_resolution_group_ac_serializer.data
                        if isinstance(problem_resolution_group_ac_serializer.data, list)
                        else problem_resolution_group_ac_serializer.data['id'],
                    'message':
                        'Información agregada correctamente'
                        if isinstance(problem_resolution_group_ac_serializer.data, list)
                        else 'Solución agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': problem_resolution_group_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Problem Resolution Group Ac
    def update(self, request, pk=None):
        problem_resolution_group_ac = self.get_object(pk)
        # Send information to serializer referencing the instance
        problem_resolution_ac_serializer = self.serializer_class(
            problem_resolution_group_ac, data=request.data
        )
        if problem_resolution_ac_serializer.is_valid():
            problem_resolution_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'conon_data': problem_resolution_ac_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': problem_resolution_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Problem Resolution Group Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_problem_resolution_group_ac(self, request, pk=None):
        problem_resolution_group_ac = self.get_object(pk)
        problem_resolution_group_ac.active = False
        problem_resolution_group_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Solución bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )

    # Get Problem Resolution by Team Detail Ac
    @action(detail=True, methods=['GET'], url_path='by-team-detail')
    def get_problem_resolution_group_by_team_detail(self, request, pk=None):
        team_detail_ac = TeamDetailAc.objects.get_team_ac_active_object_queryset(pk=pk)
        if team_detail_ac is not None:
            problem_resolution = self.serializer_class().Meta.model.objects.\
                get_problem_resolution_by_team(team=team_detail_ac.team_ac)
            if problem_resolution is not None:
                problem_resolution_serializer = self.list_serializer_class(
                    problem_resolution.first()
                )

                return Response(
                    {
                        'ok': True,
                        'conon_data': problem_resolution_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar la solución del problema.'
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

