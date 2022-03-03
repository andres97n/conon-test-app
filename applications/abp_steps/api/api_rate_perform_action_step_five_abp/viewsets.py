
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import (RatePerformActionStepFiveAbpSerializer,
                          RatePerformActionStepFiveAbpListSerializer)


class RatePerformActionStepFiveAbpViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = RatePerformActionStepFiveAbpSerializer
    list_serializer_class = RatePerformActionStepFiveAbpListSerializer
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.\
            get_rate_perform_action_abp_list()

    # Get Rate Perform Action List
    def list(self, request):
        rate_perform_action_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(rate_perform_action_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        rate_perform_action_serializer = self.list_serializer_class(
            rate_perform_action_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': rate_perform_action_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Update Rate Perform Action ABP
    def update(self, request, pk=None):
        rate_abp = self.get_object(pk)
        # Send information to serializer referencing the instance
        rate_perform_action_serializer = self.serializer_class(rate_abp, data=request.data)
        if rate_perform_action_serializer.is_valid():
            rate_perform_action_serializer.save()
            return Response(
                {
                    'ok': True,
                    'conon_data': rate_perform_action_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': rate_perform_action_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Rate Perform Action ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_rate_perform_action_abp(self, request, pk=None):
        rate_perform_action_abp = self.get_object(pk)
        rate_perform_action_abp.active = False
        rate_perform_action_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Calificación bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
