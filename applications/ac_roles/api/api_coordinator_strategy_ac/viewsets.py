
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import CoordinatorStrategyAcSerializer, CoordinatorStrategyListAcSerializer


class CoordinatorStrategyAcViewSet(viewsets.GenericViewSet):
    serializer_class = CoordinatorStrategyAcSerializer
    list_serializer_class = CoordinatorStrategyListAcSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_coordinator_strategy_ac_active_queryset(),
            id=pk
        )

    # Return Coordinator Strategy Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_coordinator_strategy_ac_list()

    # Get Coordinator Strategy Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        coordinator_strategy_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': coordinator_strategy_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Coordinator Strategy Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        coordinator_strategy_ac_serializer = self.get_serializer(data=request.data, many=is_many)
        if coordinator_strategy_ac_serializer.is_valid():
            coordinator_strategy_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'coordinator_strategy_ac':
                        coordinator_strategy_ac_serializer.data
                        if isinstance(coordinator_strategy_ac_serializer.data, list)
                        else coordinator_strategy_ac_serializer.data['id'],
                    'message':
                        'Estrategias agregadas correctamente'
                        if isinstance(coordinator_strategy_ac_serializer.data, list)
                        else 'Estrategia agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': coordinator_strategy_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Coordinator Strategy Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_coordinator_strategy_ac(self, request, pk=None):
        coordinator_strategy_ac = self.get_object(pk)
        coordinator_strategy_ac.active = False
        coordinator_strategy_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Estrategia bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
