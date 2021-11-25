from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import AsignatureClassroomSerializer, AsignatureClassroomByAsignature
from applications.base.paginations import CononPagination


class AsignatureClassroomViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = AsignatureClassroomSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_asignature_classroom_list()
        return self.get_serializer().Meta.model.objects.get_asignature_classroom_by_id(pk)

    # Get Asignature Classroom List
    def list(self, request, *args, **kwargs):
        asignature_classroom_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(asignature_classroom_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        asignature_classroom_serializer = self.get_serializer(asignature_classroom_queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': asignature_classroom_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Asignature Classroom Data
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        asignature_classroom_serializer = self.get_serializer(data=request.data)
        if asignature_classroom_serializer.is_valid():
            asignature_classroom_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': asignature_classroom_serializer.data['id'],
                    'message': 'Valores creados correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': asignature_classroom_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Asignature Classroom Data
    def update(self, request, pk=None, *args, **kwargs):
        asignature_classroom = self.get_queryset(pk)
        if asignature_classroom:
            # Send information to serializer referencing the instance
            asignature_classroom_serializer = self.get_serializer(asignature_classroom, data=request.data)
            if asignature_classroom_serializer.is_valid():
                asignature_classroom_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': asignature_classroom_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': asignature_classroom_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Asignature Classroom Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            asignature_classroom_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': asignature_classroom_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Registro.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Asignature Classroom Data
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        asignature_classroom = self.get_queryset(pk)
        if asignature_classroom:
            asignature_classroom.state = 0
            asignature_classroom.auth_state = 'I'
            asignature_classroom.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Registro eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Registro.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['GET'], url_path='by-asignatures')
    def get_asignatures_detail_by_asignature(self, request, pk=None):
        asignatures_detail = self.get_serializer().Meta.model.objects.get_asignature_classroom_by_asignature(pk=pk)

        if asignatures_detail is not None:
            if len(asignatures_detail) > 0:
                asignatures_detail_serializer = AsignatureClassroomByAsignature(asignatures_detail, many=True)
                asignatures_detail_data = asignatures_detail_serializer.data
            else:
                asignatures_detail_data = []
            return Response(
                {
                    'ok': True,
                    'conon_data': asignatures_detail_data
                }
            )
        else:

            return Response(
                {
                    'ok': False,
                    'detail': 'No existen registros para esta asignatura.'
                }
            )
