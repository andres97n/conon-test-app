from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from applications.school.api.api_classroom.serializers import ClassroomSerializer
from applications.base.paginations import CononPagination


class ClassroomViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = ClassroomSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Get Classroom Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_classroom_list()
        return self.get_serializer().Meta.model.objects.get_classroom_by_id(pk)

    # Get Classroom List
    def list(self, request, *args, **kwargs):
        classroom_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(classroom_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        classroom_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': classroom_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Classroom
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        classroom_serializer = self.get_serializer(data=request.data)
        if classroom_serializer.is_valid():
            classroom_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Aula creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': classroom_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Classroom
    def update(self, request, pk=None, *args, **kwargs):
        classroom = self.get_queryset(pk)
        if classroom:
            # Send information to serializer referencing the instance
            classroom_serializer = self.get_serializer(classroom, data=request.data)
            if classroom_serializer.is_valid():
                classroom_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': classroom_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': classroom_serializer.errors,
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

    # Detail Classroom Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            classroom_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': classroom_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Classroom
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        classroom = self.get_queryset(pk)
        if classroom:
            classroom.auth_state = 'I'
            classroom.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Aula eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
