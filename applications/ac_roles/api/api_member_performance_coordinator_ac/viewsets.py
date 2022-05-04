
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import MemberPerformanceCoordinatorAcSerializer, \
    MemberPerformanceCoordinatorAcSerializerList


class MemberPerformanceCoordinatorAcViewSet(viewsets.GenericViewSet):
    serializer_class = MemberPerformanceCoordinatorAcSerializer
    list_serializer_class = MemberPerformanceCoordinatorAcSerializerList
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_member_performance_ac_active_queryset(),
            id=pk
        )

    # Return Member Performance Coordinator Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_member_performance_ac_list()

    # Get Member Performance Coordinator Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        member_performance_coordinator_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': member_performance_coordinator_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Member Performance Coordinator Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        member_performance_coordinator_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if member_performance_coordinator_ac_serializer.is_valid():
            member_performance_coordinator_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'member_performance_ac':
                        member_performance_coordinator_ac_serializer.data
                        if isinstance(member_performance_coordinator_ac_serializer.data, list)
                        else member_performance_coordinator_ac_serializer.data['id'],
                    'message':
                        'Información agregada correctamente'
                        if isinstance(member_performance_coordinator_ac_serializer.data, list)
                        else 'Valoración agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': member_performance_coordinator_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Member Performance Coordinator Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_member_performance_coordinator_ac(self, request, pk=None):
        member_performance_coordinator_ac = self.get_object(pk)
        member_performance_coordinator_ac.active = False
        member_performance_coordinator_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Valoración bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
