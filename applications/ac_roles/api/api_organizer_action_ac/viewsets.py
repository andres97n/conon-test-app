

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import OrganizerActionAcSerializer, OrganizerActionAcListSerializer


class OrganizerActionAcViewSet(viewsets.GenericViewSet):
    serializer_class = OrganizerActionAcSerializer
    list_serializer_class = OrganizerActionAcListSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_organizer_action_ac_active_queryset(),
            id=pk
        )

    # Return Organizer Action Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_organizer_action_ac_list()

    # Get Organizer Action Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        organizer_action_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': organizer_action_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Organizer Action Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        organizer_action_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if organizer_action_ac_serializer.is_valid():
            organizer_action_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'organizer_action_ac':
                        organizer_action_ac_serializer.data
                        if isinstance(organizer_action_ac_serializer.data, list)
                        else organizer_action_ac_serializer.data['id'],
                    'message':
                        'Acciones creadas correctamente'
                        if isinstance(organizer_action_ac_serializer.data, list)
                        else 'Acción agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': organizer_action_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Organizer Action Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_organizer_action_ac(self, request, pk=None):
        organizer_action_ac = self.get_object(pk)
        organizer_action_ac.active = False
        organizer_action_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Acción bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
