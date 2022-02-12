from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.base.paginations import CononPagination
from applications.base.permissions import IsStudent
from applications.abp_steps.api.api_opinion_step_one_abp.serializers import \
    OpinionStepOneAbpSerializer


# TODO: Reformar este viewset a uno que no sea model viewset
class OpinionStepOneAbpViewSet(viewsets.ModelViewSet):
    serializer_class = OpinionStepOneAbpSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination

    # Get Opinion ABP Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_opinion_abp_list()
        return self.get_serializer().Meta.model.objects.get_opinion_abp_by_pk(pk)

    # Get Opinion ABP List
    def list(self, request, *args, **kwargs):
        opinion_abp_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(opinion_abp_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        opinion_abp_serializer = self.get_serializer(opinion_abp_queryset, many=True)
        return Response(
            {
                'ok': True,
                'conon_data': opinion_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Opinion ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        opinion_abp_serializer = self.get_serializer(data=request.data)
        if opinion_abp_serializer.is_valid():
            opinion_abp_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': opinion_abp_serializer.data['id'],
                    'message': 'Opinion creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': opinion_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Opinion ABP
    def update(self, request, pk=None, *args, **kwargs):
        opinion_abp = self.get_queryset(pk)
        if opinion_abp:
            # Send information to serializer referencing the instance
            opinion_abp_serializer = self.get_serializer(opinion_abp, data=request.data)
            if opinion_abp_serializer.is_valid():
                opinion_abp_serializer.save()
                return Response(
                    {
                        'ok': True,
                        'conon_data': opinion_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'ok': False,
                    'detail': opinion_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se encontró la opinión enviada.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Opinion ABP Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            opinion_abp_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': opinion_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se encontró esta Opinión.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Opinion ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        opinion_abp = self.get_queryset(pk)
        if opinion_abp:
            opinion_abp.active = False
            opinion_abp.auth_state = 'I'
            opinion_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Opinión eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró esta Opinión.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Opinion ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_opinion_abp(self, request, pk=None):
        opinion_abp = self.get_queryset(pk)
        if opinion_abp:
            opinion_abp.active = False
            opinion_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Opinión bloqueada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró esta Opinión.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create Many Opinions ABP
    @action(detail=False, methods=['POST'], url_path='create-many')
    def create_many_opinion_abp(self, request):
        is_many = True if isinstance(request.data, list) else False
        opinion_abp_serializer = self.get_serializer(data=request.data, many=is_many)
        if opinion_abp_serializer.is_valid():
            opinion_abp_serializer.save()
            return Response(
                {
                    'ok': True,
                    'opinions': opinion_abp_serializer.data,
                    'message': 'Opiniones generadas correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': opinion_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

