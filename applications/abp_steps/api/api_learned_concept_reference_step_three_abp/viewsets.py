from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import (LearnedConceptReferenceStepThreeAbpSerializer,
                          LearnedConceptReferenceListStepThreeAbpSerializer)


class LearnedConceptReferenceStepThreeAbpViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = LearnedConceptReferenceStepThreeAbpSerializer
    list_serializer_class = LearnedConceptReferenceListStepThreeAbpSerializer
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects. \
            get_learned_concept_reference_list()

    # Get Learned Concept Reference List
    def list(self, request):
        learned_concept_referencequeryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(learned_concept_referencequeryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        learned_concept_reference_serializer = self.list_serializer_class(
            learned_concept_referencequeryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': learned_concept_reference_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Update Learned Concept Reference ABP
    def update(self, request, pk=None):
        learned_concept_reference_abp = self.get_object(pk)
        # Send information to serializer referencing the instance
        learned_concept_reference_serializer = self.serializer_class(
            learned_concept_reference_abp,
            data=request.data
        )
        if learned_concept_reference_serializer.is_valid():
            learned_concept_reference_serializer.save()
            return Response(
                {
                    'ok': True,
                    'conon_data': learned_concept_reference_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': learned_concept_reference_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Learned Concept Reference ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_learned_concept_reference_abp(self, request, pk=None):
        learned_concept_reference_abp = self.get_object(pk)
        learned_concept_reference_abp.active = False
        learned_concept_reference_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Enlace bloqueado correctamente.'
            },
            status=status.HTTP_200_OK
        )
