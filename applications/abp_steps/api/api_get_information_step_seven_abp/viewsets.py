
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import (GetInformationStepSevenAbpSerializer,
                          GetInformationStepSevenAbpListSerializer)


class GetInformationStepSevenAbpViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = GetInformationStepSevenAbpSerializer
    list_serializer_class = GetInformationStepSevenAbpListSerializer
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.\
            get_information_step_seven_list()

    # Get Information Model List
    def list(self, request):
        get_information_model_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(get_information_model_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        get_information_model_serializer = self.list_serializer_class(
            get_information_model_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': get_information_model_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Get Information Model ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        get_information_model_serializer = self.get_serializer(data=request.data)
        if get_information_model_serializer.is_valid():
            get_information_model_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': get_information_model_serializer.data['id'],
                    'message': 'Información creada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': get_information_model_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Get Information Model ABP
    def update(self, request, pk=None):
        get_information_model_abp = self.get_object(pk)
        # Send information to serializer referencing the instance
        get_information_model_serializer = self.serializer_class(
            get_information_model_abp, data=request.data
        )
        if get_information_model_serializer.is_valid():
            get_information_model_serializer.save()
            return Response(
                {
                    'ok': True,
                    'conon_data': get_information_model_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': get_information_model_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Get Information Data ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_get_information_abp(self, request, pk=None):
        get_information_model_abp = self.get_object(pk)
        get_information_model_abp.active = False
        get_information_model_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Información bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
