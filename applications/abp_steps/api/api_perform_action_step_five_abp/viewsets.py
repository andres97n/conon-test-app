
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import (PerformActionStepFiveAbpSerializer,
                          PerformActionStepFiveAbpListSerializer)
from applications.abp_steps.models import RatePerformActionStepFiveAbp


class PerformActionStepFiveAbpViewSet(LoggingMixin, viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = PerformActionStepFiveAbpSerializer
    list_serializer_class = PerformActionStepFiveAbpListSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.\
            get_perform_action_abp_list()

    # Get Perform Action List
    def list(self, request):
        perform_action_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(perform_action_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        perform_action_serializer = self.list_serializer_class(
            perform_action_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': perform_action_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Unknown Concept ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        perform_action_serializer = self.get_serializer(data=request.data, many=is_many)
        if perform_action_serializer.is_valid():
            perform_action_serializer.save()
            return Response(
                {
                    'ok': True,
                    'perform_action':
                        perform_action_serializer.data
                        if isinstance(perform_action_serializer.data, list)
                        else perform_action_serializer.data['id'],
                    'message':
                        'Estrategias creadas correctamente'
                        if isinstance(perform_action_serializer.data, list)
                        else 'Estrategia creada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': perform_action_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Perform Action ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_perform_action_abp(self, request, pk=None):
        perform_action_abp = self.get_object(pk)
        perform_action_abp.active = False
        perform_action_abp.save()
        rates = RatePerformActionStepFiveAbp.objects. \
            get_rate_perform_action_list_by_action(
                perform_action_abp.id, active=False
            )
        if rates is not None:
            for rate in rates:
                rate.active = False
                rate.save()

        return Response(
            {
                'ok': True,
                'message': 'Estrategia bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )


