from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from applications.base.paginations import CononPagination
from applications.base.permissions import IsStudent
from .serializers import InteractionStepOneAbpSerializer


# TODO: Reformar este viewset a uno que no sea model viewset
class InteractionStepOneAbpViewSet(viewsets.ModelViewSet):
    serializer_class = InteractionStepOneAbpSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['opinion_step_one_abp', 'active']

    # Get Interaction ABP Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_interaction_abp_list()
        return self.get_serializer().Meta.model.objects.get_interaction_abp_by_pk(pk)

    # Get Interaction ABP List
    def list(self, request, *args, **kwargs):
        interaction_abp_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(interaction_abp_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        interaction_abp_serializer = self.get_serializer(interaction_abp_queryset, many=True)
        return Response(
            {
                'ok': True,
                'conon_data': interaction_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Interaction ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        interaction_abp_serializer = self.get_serializer(data=request.data)
        if interaction_abp_serializer.is_valid():
            interaction_abp_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': interaction_abp_serializer.data['id'],
                    'message': 'Interacción creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': interaction_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Interaction ABP
    def update(self, request, pk=None, *args, **kwargs):
        interaction_abp = self.get_queryset(pk)
        if interaction_abp:
            # Send information to serializer referencing the instance
            interaction_abp_serializer = self.get_serializer(interaction_abp, data=request.data)
            if interaction_abp_serializer.is_valid():
                interaction_abp_serializer.save()
                return Response(
                    {
                        'ok': True,
                        'conon_data': interaction_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'ok': False,
                    'detail': interaction_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se encontró la referencia enviada.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Interaction ABP Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            interaction_abp_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': interaction_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se encontró la referencia enviada.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Interaction ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        interaction_abp = self.get_queryset(pk)
        if interaction_abp:
            interaction_abp.active = False
            interaction_abp.auth_state = 'I'
            interaction_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Interacción eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró la referencia enviada.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Interaction ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_interaction_abp(self, request, pk=None):
        interaction_abp = self.get_queryset(pk)
        if interaction_abp:
            interaction_abp.active = False
            interaction_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Interacción bloqueada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró la referencia enviada.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
