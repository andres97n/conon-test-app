from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from applications.school.api.api_knowledge_area.serializers import KnowledgeAreaSerializer, \
    KnowledgeAreaByAsignature, KnowledgeAreaTeachersSerializer, TeacherByAreaListSerializer
from applications.users.models import Teacher
from applications.users.api.api_teacher.serializers import TeachersShortSerializer


class KnowledgeAreaViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = KnowledgeAreaSerializer
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Get Knowledge Area Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_area_list()
        return self.get_serializer().Meta.model.objects.get_are_by_id(pk)

    # Get KnowledgeArea List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        conversation_detail_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': conversation_detail_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Knowledge Area
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        knowledge_area_serializer = self.get_serializer(data=request.data)
        if knowledge_area_serializer.is_valid():
            knowledge_area_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': knowledge_area_serializer.data['id'],
                    'message': 'Área de Conocimiento creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': knowledge_area_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Knowledge Area
    def update(self, request, pk=None, *args, **kwargs):
        knowledge_area = self.get_queryset(pk)
        if knowledge_area:
            # Send information to serializer referencing the instance
            knowledge_area_serializer = self.get_serializer(knowledge_area, data=request.data)
            if knowledge_area_serializer.is_valid():
                knowledge_area_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': knowledge_area_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': knowledge_area_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Área de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Knowledge Area
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            knowledge_area_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': knowledge_area_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Área de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Knowledge Area
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        knowledge_area = self.get_queryset(pk)
        if knowledge_area is not None:
            knowledge_area.auth_state = 'I'
            knowledge_area.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Área de Conocimiento eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Área de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['POST'], url_path='assign-teachers')
    def save_teachers_by_area(self, request, pk=None):
        knowledge_area = self.get_queryset(pk)

        if knowledge_area is not None:
            if request.data['teachers']:
                for teacher in request.data['teachers']:
                    knowledge_area.teachers.add(teacher)
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar a los Docente/s.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    'ok': True,
                    'message': 'Docente/s agregados correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Área de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Return Teachers by Knowledge Area
    @action(detail=True, methods=['GET'], url_path='teachers')
    def get_teachers_by_area(self, request, pk=None):
        teachers = self.get_serializer().Meta.model.objects.get_teachers_by_area_id(pk=pk)
        if teachers is not None:

            if self.get_serializer().Meta.model.objects.get_teachers_count(pk=pk) == 0:
                area_teacher_serializer = TeacherByAreaListSerializer(teachers, many=True)
                return Response(
                    {
                        'ok': True,
                        'conon_data': area_teacher_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': True,
                        'message': 'La siguiente Área de Conocimiento no contiene Docentes.'
                    },
                    status=status.HTTP_200_OK
                )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se encontró el Área de Conocimiento.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # Delete Many Areas
    @action(detail=False, methods=['DELETE'], url_path='destroy-areas')
    def destroy_areas(self, request):
        areas = self.get_serializer().Meta.model.objects.get_many_areas(areas=request.data['areas'])
        if areas:
            for area in areas:
                area.auth_state = 'I'

            self.get_serializer().Meta.model.objects.bulk_update(areas, ['auth_state'])

            return Response(
                {
                    'ok': True,
                    'message': 'Áreas de Conocimiento eliminadas correctamente.'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se puede eliminar las siguientes Áreas de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get Areas for the Asignatures
    @action(detail=False, methods=['GET'], url_path='asignature')
    def get_areas_asignature(self, request):
        areas = self.get_queryset()
        if areas:
            area_serializer = KnowledgeAreaByAsignature(areas, many=True)
            return Response(
                {
                    'ok': True,
                    'conon_data': area_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se puedo retornar las Áreas de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['GET'], url_path='teachers')
    def get_area_teachers(self, request):
        teachers = self.get_serializer().Meta.model.objects.get_teachers_area()
        if teachers:
            teacher_serializer = KnowledgeAreaTeachersSerializer(teachers, many=True)

            return Response(
                {
                    'ok': True,
                    'conon_data': teacher_serializer.data
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

    @action(detail=True, methods=['GET'], url_path='new-teachers')
    def get_new_teachers_for_area(self, request, pk=None):
        teachers = self.get_serializer().Meta.model.objects.get_teachers_by_area_id(pk=pk)
        if teachers is not None:
            teacher_serializer = TeachersShortSerializer(
                Teacher.objects.get_teachers_short_data(), many=True
            )
            area_teacher_serializer = TeacherByAreaListSerializer(teachers, many=True)
            valid_teachers = [
                teacher for teacher in teacher_serializer.data
                if teacher not in area_teacher_serializer.data
            ]
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
