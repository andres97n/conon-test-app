
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import (ProblemDefinitionReferenceStepSixAbpSerializer,
                          ProblemDefinitionReferenceStepSixAbpListSerializer)


class ProblemDefinitionReferenceStepSixAbpViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = ProblemDefinitionReferenceStepSixAbpSerializer
    list_serializer_class = ProblemDefinitionReferenceStepSixAbpListSerializer
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_abp', 'active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.\
            get_problem_definition_references_list()

    # Get Problem Definition Reference List
    def list(self, request):
        problem_definition_reference_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(problem_definition_reference_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        problem_definition_reference_serializer = self.list_serializer_class(
            problem_definition_reference_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': problem_definition_reference_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Problem Definition Reference ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        problem_definition_reference_serializer = self.get_serializer(data=request.data)
        if problem_definition_reference_serializer.is_valid():
            problem_definition_reference_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': problem_definition_reference_serializer.data['id'],
                    'message': 'Referencia creada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': problem_definition_reference_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Problem Definition Reference ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_problem_definition_reference_abp(self, request, pk=None):
        problem_definition_reference_abp = self.get_object(pk)
        problem_definition_reference_abp.active = False
        problem_definition_reference_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Referencia bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )

