from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import RubricAbpSerializer
from applications.base.permissions import IsOwnerAndTeacher
from applications.base.paginations import CononPagination


class RubricAbpViewSet(viewsets.ModelViewSet):
    serializer_class = RubricAbpSerializer
    permission_classes = [IsOwnerAndTeacher]
    pagination_class = CononPagination

    # Return Rubric ABP
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_rubric_abp_list()
        return self.get_serializer().Meta.model.objects.get_rubric_abp_by_id(pk)

    # Get Rubric ABP List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        rubric_abp_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': rubric_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Rubric ABP
    def create(self, request, *args, **kwargs):
        rubric_abp_serializer = self.get_serializer(data=request.data)
        if rubric_abp_serializer.is_valid():
            rubric_abp_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Rúbrica creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': rubric_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Rubric ABP
    def update(self, request, pk=None, *args, **kwargs):
        rubric_abp = self.get_queryset(pk)
        if rubric_abp:
            # Send information to serializer referencing the instance
            rubric_abp_serializer = self.get_serializer(rubric_abp, data=request.data)
            if rubric_abp_serializer.is_valid():
                rubric_abp_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': rubric_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': rubric_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Rúbrica.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Rubric ABP
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            rubric_abp_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': rubric_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Rúbrica.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Rubric ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        rubric_abp = self.get_queryset(pk)
        if rubric_abp:
            rubric_abp.auth_state = 'I'
            rubric_abp.state = 0
            rubric_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Rúbrica eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Rúbrica.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

