from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import EvaluationAbpSerializer
from applications.base.permissions import IsOwnerAndTeacher
from applications.base.paginations import CononPagination


class EvaluationAbpViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationAbpSerializer
    permission_classes = [IsOwnerAndTeacher]
    pagination_class = CononPagination

    # Return Team ABP
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_evaluation_abp_list()
        return self.get_serializer().Meta.model.objects.get_evaluation_abp_by_id(pk)

    # Get Evaluation ABP List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        evaluation_abp_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': evaluation_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Evaluation ABP
    def create(self, request, *args, **kwargs):
        evaluation_abp_serializer = self.get_serializer(data=request.data)
        if evaluation_abp_serializer.is_valid():
            evaluation_abp_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Evaluación creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': evaluation_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Evaluation ABP
    def update(self, request, pk=None, *args, **kwargs):
        evaluation_abp = self.get_queryset(pk)
        if evaluation_abp:
            # Send information to serializer referencing the instance
            evaluation_abp_serializer = self.get_serializer(evaluation_abp, data=request.data)
            if evaluation_abp_serializer.is_valid():
                evaluation_abp_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': evaluation_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': evaluation_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Evaluación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Evaluation ABP
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            evaluation_abp_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': evaluation_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Evaluación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Evaluation ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        evaluation_abp = self.get_queryset(pk)
        if evaluation_abp:
            evaluation_abp.auth_state = 'I'
            evaluation_abp.state = 0
            evaluation_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Evaluación eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Evaluación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

