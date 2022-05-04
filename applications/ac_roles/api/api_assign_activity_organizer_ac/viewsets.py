
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import AssignActivityOrganizerAcSerializer, AssignActivityOrganizerAcListSerializer


class AssignActivityOrganizerAcViewSet(viewsets.GenericViewSet):
    serializer_class = AssignActivityOrganizerAcSerializer
    list_serializer_class = AssignActivityOrganizerAcListSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_ac', 'member_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_assign_activity_organizer_ac_active_queryset(),
            id=pk
        )

    # Return Assign Activity Organizer Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_assign_activity_organizer_ac_list()

    # Get Assign Activity Organizer Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        assign_activity_organizer_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': assign_activity_organizer_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Assign Activity Organizer Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        assign_activity_organizer_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if assign_activity_organizer_ac_serializer.is_valid():
            assign_activity_organizer_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'assign_activity_ac':
                        assign_activity_organizer_ac_serializer.data
                        if isinstance(assign_activity_organizer_ac_serializer.data, list)
                        else assign_activity_organizer_ac_serializer.data['id'],
                    'message':
                        'Asignaciones agregadas correctamente'
                        if isinstance(assign_activity_organizer_ac_serializer.data, list)
                        else 'Asignación agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': assign_activity_organizer_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Assign Activity Organizer Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_assign_activity_organizer_ac(self, request, pk=None):
        assign_activity_organizer_ac = self.get_object(pk)
        assign_activity_organizer_ac.active = False
        assign_activity_organizer_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Asignación bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
