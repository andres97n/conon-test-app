from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.paginations import CononPagination
from applications.base.permissions import IsTeacher
from applications.users.models import Teacher
from .serializers import AsignatureClassroomSerializer, AsignatureClassroomByAsignature


class AsignatureClassroomViewSet(LoggingMixin, viewsets.ModelViewSet):
    # permission_classes = ([IsAdminUser])
    serializer_class = AsignatureClassroomSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['classroom', 'asignature', 'teacher', 'state']

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_asignature_classroom_list()
        return self.get_serializer().Meta.model.objects.get_asignature_classroom_by_id(pk)

    def get_permissions(self):
        if self.action == 'list' or 'get_asignature_classroom_list_by_classrooms_and_teacher':
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAdminUser]

        return [permission() for permission in self.permission_classes]

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
                    'message': 'Asignación creada correctamente.'
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

    # PROVISIONAL
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

    @action(detail=False, methods=['POST'], url_path='by-classroom-and-user')
    def get_asignature_classroom_list_by_classrooms_and_teacher(self, request):

        if request.data:
            teacher_id = Teacher.objects.get_teacher_by_user(pk=request.data['user'])

            if teacher_id is not None:
                asignature_classroom = self.get_serializer().Meta.model.objects.get_asignature_classroom_by_classroom_and_teacher(
                    classroom_id=request.data['classroom'],
                    teacher_id=teacher_id['id']
                )

                if asignature_classroom is not None:
                    asignatures_detail_serializer = self.get_serializer(asignature_classroom, many=True)

                    return Response(
                        {
                            'ok': True,
                            'conon_data': asignatures_detail_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontró ningún registro.'
                        }
                    )

            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró ningún Docente.'
                    }
                )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se encuentró los atributos necesarios para el filtro.'
                }
            )

    @action(detail=True, methods=['DELETE'], url_path='block-asignature-classroom')
    def block_asignature_classroom(self, request, pk=None):
        asignature_classroom = self.get_queryset(pk)
        if asignature_classroom:
            asignature_classroom.state = 0
            asignature_classroom.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Asignación bloqueada correctamente.'
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

