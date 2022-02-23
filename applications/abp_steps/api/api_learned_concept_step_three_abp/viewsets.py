from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import (LearnedConceptStepThreeAbpSerializer,
                          LearnedConceptListStepThreeAbpSerializer)
from applications.abp_steps.models import LearnedConceptReferenceStepThreeAbp


class LearnedConceptStepThreeAbpViewSet(LoggingMixin, viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = LearnedConceptStepThreeAbpSerializer
    list_serializer_class = LearnedConceptListStepThreeAbpSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.\
            get_learned_concept_list()

    # Get Learned Concept List
    def list(self, request):
        learned_concept_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(learned_concept_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        learned_concept_serializer = self.list_serializer_class(
            learned_concept_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': learned_concept_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Learned Concept ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        learned_concept_serializer = self.get_serializer(data=request.data, many=is_many)
        if learned_concept_serializer.is_valid():
            learned_concept_serializer.save()
            return Response(
                {
                    'ok': True,
                    'student_idea':
                        learned_concept_serializer.data
                        if isinstance(learned_concept_serializer.data, list)
                        else learned_concept_serializer.data['id'],
                    'message':
                        'Conceptos creados correctamente'
                        if isinstance(learned_concept_serializer.data, list)
                        else 'Concepto creado correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': learned_concept_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Learned Concept ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_learned_concept_abp(self, request, pk=None):
        learned_concept_abp = self.get_object(pk)
        learned_concept_abp.active = False
        learned_concept_abp.save()

        concept_references = LearnedConceptReferenceStepThreeAbp.objects. \
            get_learned_concept_reference_by_concept(learned_concept_abp.id)
        if concept_references is not None:
            for reference in concept_references:
                reference.active = False
                reference.save()

        return Response(
            {
                'ok': True,
                'message': 'Concepto bloqueado correctamente.'
            },
            status=status.HTTP_200_OK
        )
