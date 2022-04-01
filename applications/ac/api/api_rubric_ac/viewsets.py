from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import RubricAcSerializer, RubricAcListSerializer
from applications.base.permissions import IsTeacher
from applications.base.paginations import CononPagination


class RubricAcViewSet(LoggingMixin, viewsets.GenericViewSet):
    serializer_class = RubricAcSerializer
    list_serializer_class = RubricAcListSerializer
    permission_classes = [IsTeacher]
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ac', 'state']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_rubric_ac_active_object_queryset(), id=pk
        )

    # Return Rubric Ac List
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_rubric_ac_list()

    # Get Rubric Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        rubric_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': rubric_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Rubric Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        rubric_ac_serializer = self.get_serializer(data=request.data)
        if rubric_ac_serializer.is_valid():
            rubric_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': rubric_ac_serializer.data['id'],
                    'message': 'Rúbrica creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': rubric_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Rubric AC
    def update(self, request, pk=None, *args, **kwargs):
        rubric_ac = self.get_object(pk)
        # Send information to serializer referencing the instance
        rubric_ac_serializer = self.get_serializer(rubric_ac, data=request.data)
        if rubric_ac_serializer.is_valid():
            rubric_ac_serializer.save()

            return Response(
                {
                    'ok': True,
                    'conon_data': rubric_ac_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': rubric_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Rubric Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_rubric_ac(self, request, pk=None):
        rubric_ac = self.get_object(pk)
        rubric_ac.active = False
        rubric_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Rúbrica bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
