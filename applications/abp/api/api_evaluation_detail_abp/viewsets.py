from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import EvaluationDetailAbpSerializer
from applications.base.permissions import IsOwnerAndTeacher


class EvaluationDetailAbpViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationDetailAbpSerializer
    permission_classes = [IsOwnerAndTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['evaluation_abp', 'active']

    # Return Rubric Detail ABP
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_evaluation_detail_abp_list()
        return self.get_serializer().Meta.model.objects.get_evaluation_detail_abp_by_id(pk)

    # Get Rubric Detail ABP List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        evaluation_detail_abp_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': evaluation_detail_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Rubric Detail ABP
    def create(self, request, *args, **kwargs):
        evaluation_detail_abp_serializer = self.get_serializer(data=request.data)
        if evaluation_detail_abp_serializer.is_valid():
            evaluation_detail_abp_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': evaluation_detail_abp_serializer.data['id'],
                    'message': 'Calificación guardada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': evaluation_detail_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Rubric Detail ABP
    def update(self, request, pk=None, *args, **kwargs):
        evaluation_detail_abp = self.get_queryset(pk)
        if evaluation_detail_abp:
            # Send information to serializer referencing the instance
            evaluation_detail_abp_serializer = self.get_serializer(evaluation_detail_abp, data=request.data)
            if evaluation_detail_abp_serializer.is_valid():
                evaluation_detail_abp_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': evaluation_detail_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': evaluation_detail_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Calificación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Rubric Detail ABP
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            evaluation_detail_abp_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': evaluation_detail_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Calificación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Rubric Detail ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        evaluation_detail_abp = self.get_queryset(pk)
        if evaluation_detail_abp:
            evaluation_detail_abp.auth_state = 'I'
            evaluation_detail_abp.active = False
            evaluation_detail_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Calificación eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Calificación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Evaluation Detail Abp
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_evaluation_detail_abp(self, request, pk=None):
        evaluation_detail_abp = self.get_queryset(pk)
        evaluation_detail_abp.active = False
        evaluation_detail_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Detalle de Evaluación bloqueado correctamente.'
            },
            status=status.HTTP_200_OK
        )
