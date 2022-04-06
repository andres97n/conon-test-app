from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import RubricDetailAbpSerializer
from applications.base.permissions import IsOwnerAndTeacher


class RubricDetailAbpViewSet(viewsets.ModelViewSet):
    serializer_class = RubricDetailAbpSerializer
    permission_classes = [IsOwnerAndTeacher]

    # Return Rubric Detail ABP
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_rubric_detail_abp_list()
        return self.get_serializer().Meta.model.objects.get_rubric_detail_abp_by_id(pk)

    # Get Rubric Detail ABP List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        rubric_detail_abp_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': rubric_detail_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Rubric Detail ABP
    def create(self, request, *args, **kwargs):
        is_many = True if isinstance(request.data, list) else False
        rubric_detail_abp_serializer = self.get_serializer(data=request.data, many=is_many)
        if rubric_detail_abp_serializer.is_valid():
            rubric_detail_abp_serializer.save()

            return Response(
                {
                    'ok': True,
                    'rubric_detail_abp':
                        rubric_detail_abp_serializer.data
                        if isinstance(rubric_detail_abp_serializer.data, list)
                        else rubric_detail_abp_serializer.data['id'],
                    'message':
                        'Secciones agregadas correctamente'
                        if isinstance(rubric_detail_abp_serializer.data, list)
                        else 'Sección agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': rubric_detail_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Rubric Detail ABP
    def update(self, request, pk=None, *args, **kwargs):
        rubric_detail_abp = self.get_queryset(pk)
        if rubric_detail_abp:
            # Send information to serializer referencing the instance
            rubric_detail_abp_serializer = self.get_serializer(rubric_detail_abp, data=request.data)
            if rubric_detail_abp_serializer.is_valid():
                rubric_detail_abp_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': rubric_detail_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': rubric_detail_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Sección.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Rubric Detail ABP
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            rubric_detail_abp_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': rubric_detail_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Sección.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Rubric Detail ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        rubric_detail_abp = self.get_queryset(pk)
        if rubric_detail_abp:
            rubric_detail_abp.auth_state = 'I'
            rubric_detail_abp.active = False
            rubric_detail_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Sección eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Sección.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

