from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from applications.base.paginations import CononPagination
from applications.base.permissions import IsTeacher
from applications.abp_steps.api.api_answer_step_one_abp.serializers import \
    AnswerStepOneAbpSerializer

# TODO: Reformar este viewset a uno que no sea model viewset


class AnswerStepOneAbpViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerStepOneAbpSerializer
    permission_classes = [IsTeacher]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['question_step_one_abp', 'user', 'active']

    # Get Answer ABP Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_answer_abp_list()
        return self.get_serializer().Meta.model.objects.get_answer_abp_by_pk(pk)

    # Get Answer ABP List
    def list(self, request, *args, **kwargs):
        answer_abp_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(answer_abp_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        answer_abp_serializer = self.get_serializer(answer_abp_queryset, many=True)
        return Response(
            {
                'ok': True,
                'conon_data': answer_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Answer ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        answer_abp_serializer = self.get_serializer(data=request.data)
        if answer_abp_serializer.is_valid():
            answer_abp_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': answer_abp_serializer.data['id'],
                    'message': 'Respuesta generada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': answer_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Answer ABP
    def update(self, request, pk=None, *args, **kwargs):
        answer_abp = self.get_queryset(pk)
        if answer_abp:
            # Send information to serializer referencing the instance
            answer_abp_serializer = self.get_serializer(answer_abp, data=request.data)
            if answer_abp_serializer.is_valid():
                answer_abp_serializer.save()
                return Response(
                    {
                        'ok': True,
                        'conon_data': answer_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'ok': False,
                    'detail': answer_abp_serializer.errors,
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

    # Detail Answer ABP Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            answer_abp_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': answer_abp_serializer.data,
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

    # Delete Answer ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        answer_abp = self.get_queryset(pk)
        if answer_abp:
            answer_abp.active = False
            answer_abp.auth_state = 'I'
            answer_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Respuesta eliminada correctamente.'
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

    # Block Answer ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_interaction_abp(self, request, pk=None):
        answer_abp = self.get_queryset(pk)
        if answer_abp:
            answer_abp.active = False
            answer_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Respuesta bloqueada correctamente.'
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
