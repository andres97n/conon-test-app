from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import (UnknownConceptReferenceStepFourAbpSerializer,
                          UnknownConceptReferenceStepFourAbpListSerializer)


class UnknownConceptReferenceStepFourAbpViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = UnknownConceptReferenceStepFourAbpSerializer
    list_serializer_class = UnknownConceptReferenceStepFourAbpListSerializer
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.\
            get_unknown_concept_reference_list()

    # Get Unknown Concept Reference List
    def list(self, request):
        unknown_concept_reference_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(unknown_concept_reference_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        unknown_concept_reference_serializer = self.list_serializer_class(
            unknown_concept_reference_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': unknown_concept_reference_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Unknown Concept Reference ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        unknown_concept_reference_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if unknown_concept_reference_serializer.is_valid():
            unknown_concept_reference_serializer.save()
            return Response(
                {
                    'ok': True,
                    'reference':
                        unknown_concept_reference_serializer.data
                        if isinstance(unknown_concept_reference_serializer.data, list)
                        else unknown_concept_reference_serializer.data['id'],
                    'message':
                        'Referencias creadas correctamente'
                        if isinstance(unknown_concept_reference_serializer.data, list)
                        else 'Referencia creada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': unknown_concept_reference_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Unknown Concept ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_unknown_concept_reference_abp(self, request, pk=None):
        unknown_concept_reference_abp = self.get_object(pk)
        unknown_concept_reference_abp.active = False
        unknown_concept_reference_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Referencia bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )

