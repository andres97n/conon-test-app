from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from applications.base.paginations import CononPagination
from .serializers import TeacherSerializer, TeacherByAreaListSerializer, \
    CoordinatorSerializer


class TeacherViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    pagination_class = CononPagination
    serializer_class = TeacherSerializer
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Return teacher data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_teacher_list()
        return self.get_serializer().Meta.model.objects.get_teacher_by_id(pk)

    # Get Teacher List
    def list(self, request, *args, **kwargs):
        teacher_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(teacher_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        teacher_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': teacher_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Teacher
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        teacher_serializer = self.get_serializer(data=request.data)
        if teacher_serializer.is_valid():
            teacher_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': teacher_serializer.data['id'],
                    'message': 'Docente creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': teacher_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Teacher
    def update(self, request, pk=None, *args, **kwargs):
        teacher = self.get_queryset(pk)
        if teacher:
            # Send information to serializer referencing the instance
            teacher_serializer = self.get_serializer(teacher, data=request.data)
            if teacher_serializer.is_valid():
                teacher_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': teacher_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': teacher_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Docente.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Teacher data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            teacher_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': teacher_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Docente.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Teacher
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        teacher = self.get_queryset(pk)
        if teacher:
            teacher.auth_state = 'I'
            teacher.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Docente eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Docente.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Many Teachers
    @action(detail=False, methods=(['DELETE']))
    def destroy_teachers(self, request):
        teachers = self.get_serializer().Meta.model.objects.get_many_teachers(request.data['teachers'])
        if teachers:
            for teacher in teachers:
                teacher.auth_state = 'I'

            self.get_serializer().Meta.model.objects.bulk_update(teachers, ['auth_state'])

            return Response(
                {
                    'ok': True,
                    'message': 'Docentes eliminados correctamente.'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se puede eliminar a estos Docentes.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=(['GET']))
    def get_coordinators(self, request):
        teachers = self.get_serializer().Meta.model.objects.get_coordinators_data()
        if teachers:
            coordinator_serializer = CoordinatorSerializer(teachers, many=True)

            return Response(
                {
                    'ok': True,
                    'conon_data': coordinator_serializer.data
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No existen Docentes.'
                },
                status=status.HTTP_200_OK
            )
