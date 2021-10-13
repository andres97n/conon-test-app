from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from applications.base.permissions import IsTeacher
from .serializers import GlosarySerializer
from applications.base.paginations import CononPagination


# The Teacher enable the Glosary for to add terms
class GlosaryViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsTeacher])
    serializer_class = GlosarySerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Return Glosary Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_glosary_list()
        return self.get_serializer().Meta.model.objects.get_glosary_by_id(pk)

    # Get Glosary List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        glosary_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': glosary_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create a Glosary
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        glosary_serializer = self.get_serializer(data=request.data)
        if glosary_serializer.is_valid():
            glosary_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Glosario creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': glosary_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Glosary
    def update(self, request, pk=None, *args, **kwargs):
        glosary = self.get_queryset(pk)
        if glosary:
            # Send information to serializer referencing the instance
            glosary_serializer = self.get_serializer(glosary, data=request.data)
            if glosary_serializer.is_valid():
                glosary_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': glosary_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': glosary_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Glosario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Glosary Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            glosary_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': glosary_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Glosario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Glosary
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        glosary = self.get_queryset(pk)
        if glosary:
            glosary.state = False
            glosary.auth_state = 'I'
            glosary.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Glosario eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Glosario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
