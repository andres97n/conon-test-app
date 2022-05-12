
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import ActivityDescriptionSpokesmanAcSerializer, ActivityDescriptionSpokesmanAcListSerializer


class ActivityDescriptionSpokesmanAcViewSet(viewsets.GenericViewSet):
    serializer_class = ActivityDescriptionSpokesmanAcSerializer
    list_serializer_class = ActivityDescriptionSpokesmanAcListSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_ac', 'member_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_activity_description_spokesman_ac_active_queryset(),
            id=pk
        )

    # Return Activity Description Spokesman Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_activity_description_spokesman_ac_list()

    # Get Activity Description Spokesman Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        activity_description_spokesman_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': activity_description_spokesman_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Activity Description Spokesman Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        activity_description_spokesman_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if activity_description_spokesman_ac_serializer.is_valid():
            activity_description_spokesman_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'activity_description_ac':
                        activity_description_spokesman_ac_serializer.data
                        if isinstance(activity_description_spokesman_ac_serializer.data, list)
                        else activity_description_spokesman_ac_serializer.data['id'],
                    'message':
                        'Descripciones agregadas correctamente'
                        if isinstance(activity_description_spokesman_ac_serializer.data, list)
                        else 'Descripción agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': activity_description_spokesman_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Activity Description Spokesman Ac
    def update(self, request, pk=None):
        activity_description_spokesman_ac = self.get_object(pk)
        # Send information to serializer referencing the instance
        activity_description_spokesman_ac_serializer = self.serializer_class(
            activity_description_spokesman_ac, data=request.data
        )
        if activity_description_spokesman_ac_serializer.is_valid():
            activity_description_spokesman_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'conon_data': activity_description_spokesman_ac_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': activity_description_spokesman_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Activity Description Spokesman Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_activity_description_spokesman_ac(self, request, pk=None):
        activity_description_spokesman_ac = self.get_object(pk)
        activity_description_spokesman_ac.active = False
        activity_description_spokesman_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Descripción bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
