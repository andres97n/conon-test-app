
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import DescribeUnderstandingOrganizerAcSerializer, DescribeUnderstandingOrganizerListAcSerializer


class DescribeUnderstandingOrganizerAcViewSet(viewsets.GenericViewSet):
    serializer_class = DescribeUnderstandingOrganizerAcSerializer
    list_serializer_class = DescribeUnderstandingOrganizerListAcSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_ac', 'member_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_describe_understanding_organizer_ac_active_queryset(),
            id=pk
        )

    # Return Describe Understanding Organizer Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_describe_understanding_organizer_ac_list()

    # Get Describe Understanding Organizer Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        describe_understanding_organizer_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': describe_understanding_organizer_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Describe Understanding Organizer Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        describe_understanding_organizer_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if describe_understanding_organizer_ac_serializer.is_valid():
            describe_understanding_organizer_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'describe_understanding_ac':
                        describe_understanding_organizer_ac_serializer.data
                        if isinstance(describe_understanding_organizer_ac_serializer.data, list)
                        else describe_understanding_organizer_ac_serializer.data['id'],
                    'message':
                        'Descripciones agregadas correctamente'
                        if isinstance(describe_understanding_organizer_ac_serializer.data, list)
                        else 'Descripción agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': describe_understanding_organizer_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Describe Understanding Organizer Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_describe_understanding_organizer_ac(self, request, pk=None):
        describe_understanding_organizer_ac = self.get_object(pk)
        describe_understanding_organizer_ac.active = False
        describe_understanding_organizer_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Descripción bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
