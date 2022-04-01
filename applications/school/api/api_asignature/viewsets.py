from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import AsignatureSerializer, AsignatureDetailSerializer
from applications.base.paginations import CononPagination
from applications.base.permissions import IsTeacher
from applications.school.models import Classroom, AsignatureClassroom, KnowledgeArea
from applications.school.api.api_classroom.serializers import ClassroomShortSerializer
from applications.school.api.api_knowledge_area.serializers import TeacherByAreaListSerializer
# from applications.users.api.api_teacher.serializers import TeachersShortSerializer


class AsignatureViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsTeacher, IsAdminUser])
    serializer_class = AsignatureSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_asignature_list()
        return self.get_serializer().Meta.model.objects.get_asignature_by_id(pk)

    # Get Classroom List
    def list(self, request, *args, **kwargs):
        asignature_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(asignature_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        asignature_serializer = self.get_serializer(asignature_queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': asignature_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Asignature
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        asignature_serializer = self.get_serializer(data=request.data)
        if asignature_serializer.is_valid():
            asignature_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': asignature_serializer.data['id'],
                    'message': 'Asignatura creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': asignature_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Asignature
    def update(self, request, pk=None, *args, **kwargs):
        asignature = self.get_queryset(pk)
        if asignature:
            # Send information to serializer referencing the instance
            asignature_serializer = self.get_serializer(asignature, data=request.data)
            if asignature_serializer.is_valid():
                asignature_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': asignature_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': asignature_serializer.errors,
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

    # Detail Asignature Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            asignature_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': asignature_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Asignatura.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Asignature
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        asignature = self.get_queryset(pk)
        if asignature:
            asignature.state = 0
            asignature.auth_state = 'I'
            asignature.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Asignatura eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Asignatura.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['DELETE'], url_path='destroy-asignatures')
    def destroy_many_asignatures(self, request):
        asignatures = self.get_serializer().Meta.model.objects.get_many_asignatures(
            asignatures=request.data['asignatures']
        )
        if asignatures:
            for asignature in asignatures:
                asignature.state = 0
                asignature.auth_state = 'I'

            self.get_serializer().Meta.model.objects.bulk_update(
                asignatures, ['state', 'auth_state']
            )

            return Response(
                {
                    'ok': True,
                    'message': 'Asignaturas eliminadas correctamente.'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se puede eliminar las siguientes Asignaturas.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['GET'], url_path='active')
    def get_asignatures_active(self, request):
        asignatures = self.get_serializer().Meta.model.objects.get_asignature_list_active()
        if asignatures:
            asignature_serializer = self.get_serializer(asignatures, many=True)
            return Response(
                {
                    'ok': True,
                    'conon_data': asignature_serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se puedo retornar las siguientes Asignaturas.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# TODO: Si es que se dispone de tiempo, se debería agregar nivel de asignatura para el filtro de las aulas

    @action(detail=True, methods=['GET'], url_path='classrooms')
    def get_asignatures_detail_classrooms(self, request, pk=None):
        asignatures = AsignatureClassroom.objects.get_asignature_classroom_by_asignature_short(pk=pk)
        if asignatures is not None:
            asignature_serializer = AsignatureDetailSerializer(asignatures, many=True)
            classroom_serializer = ClassroomShortSerializer(
                Classroom.objects.get_short_classroom(), many=True
            )
            asignature_keys = {asignature['classroom'] for asignature in asignature_serializer.data}
            if len(asignatures) != 0:
                valid_classrooms = [
                    classroom for classroom in classroom_serializer.data
                    if classroom['id'] not in asignature_keys
                ]
            else:
                valid_classrooms = classroom_serializer.data
            return Response(
                {
                    'ok': True,
                    'conon_data': valid_classrooms
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se pudo cargar las Aulas.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['GET'], url_path='teachers')
    def get_asignatures_detail_teachers(self, request, pk=None):
        asignatures = AsignatureClassroom.objects.get_asignature_classroom_by_asignature_short(pk=pk)
        if asignatures is not None:
            # asignature_serializer = AsignatureDetailSerializer(asignatures, many=True)
            area_id = self.get_queryset(pk)
            teacher_serializer = TeacherByAreaListSerializer(
                KnowledgeArea.objects.get_teachers_by_area_id(area_id.knowledge_area.id),
                many=True
            )
            """
            teacher_serializer = TeachersShortSerializer(
                Teacher.objects.get_teachers_short_data(), many=True
            )
            
            asignature_keys = {asignature['teacher'] for asignature in asignature_serializer.data}
            if len(asignatures) != 0:
                valid_teachers = [
                    teacher for teacher in teacher_serializer.data
                    if teacher['id'] not in asignature_keys
                ]
            else:
                valid_teachers = teacher_serializer.data
            """
            valid_teachers = teacher_serializer.data

            return Response(
                {
                    'ok': True,
                    'conon_data': valid_teachers
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se pudo cargar los Docentes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
