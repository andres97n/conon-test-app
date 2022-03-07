
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import (ProblemResolutionStepEightAbpSerializer,
                          ProblemResolutionStepEightAbpListSerializer)


class ProblemResolutionStepEightAbpViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = ProblemResolutionStepEightAbpSerializer
    list_serializer_class = ProblemResolutionStepEightAbpListSerializer
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_abp', 'active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.\
            get_problem_resolution_step_eight_list()

    # Get Problem Resolution List
    def list(self, request):
        problem_resolution_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(problem_resolution_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        problem_resolution_serializer = self.list_serializer_class(
            problem_resolution_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': problem_resolution_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Problem Resolution ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        problem_resolution_serializer = self.get_serializer(data=request.data)
        if problem_resolution_serializer.is_valid():
            problem_resolution_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': problem_resolution_serializer.data['id'],
                    'message': 'Resolución de Problema creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': problem_resolution_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Problem Resolution ABP
    def update(self, request, pk=None):
        problem_resolution_abp = self.get_object(pk)
        # Send information to serializer referencing the instance
        problem_resolution_serializer = self.serializer_class(
            problem_resolution_abp, data=request.data
        )
        if problem_resolution_serializer.is_valid():
            problem_resolution_serializer.save()
            return Response(
                {
                    'ok': True,
                    'conon_data': problem_resolution_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': problem_resolution_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Problem Resolution ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_get_information_abp(self, request, pk=None):
        problem_resolution_abp = self.get_object(pk)
        problem_resolution_abp.active = False
        problem_resolution_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Resolución bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
