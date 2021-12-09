from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TopicSerializer
from applications.base.permissions import IsOwnerAndTeacher
from applications.base.paginations import CononShortPagination
# from applications.topic.filters import TopicFilterSet
from applications.dua.models import Dua
from applications.users.models import Student, Teacher
from applications.users.api.api_student.serializers import StudentShortListSerializer
from applications.school.api.api_classroom.serializers import StudentsForManyChoicesSerializer


class TopicViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsOwnerAndTeacher])
    serializer_class = TopicSerializer
    pagination_class = CononShortPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner', 'type', 'active']

    # filter_class = TopicFilterSet

    # Return Topic Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_topic_list()
        return self.get_serializer().Meta.model.objects.get_topic_by_id(pk)

    # Get Topic List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        topic_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': topic_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create a Topic
    def create(self, request, *args, **kwargs):
        topic_serializer = self.get_serializer(data=request.data)
        if topic_serializer.is_valid():
            topic_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Tema creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': topic_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update a Topic
    def update(self, request, pk=None, *args, **kwargs):
        topic = self.get_queryset(pk)
        if topic:
            # Send information to serializer referencing the instance
            topic_serializer = self.get_serializer(topic, data=request.data)
            if topic_serializer.is_valid():
                topic_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': topic_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': topic_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Topic
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            topic_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': topic_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Topic
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        topic = self.get_queryset(pk)
        if topic is not None:
            topic.active = False
            topic.auth_state = 'I'

            if topic.type == 1:
                topic_dua = Dua.objects.get_dua_by_topic(pk)
                # TODO: Eliminar cuando se tenga todas las metodologías
                if topic_dua is not None:

                    topic_dua.state = 0
                    topic_dua.auth_state = 'I'
                    topic_dua.save()
                    topic.save()

                    return Response(
                        {
                            'ok': True,
                            'message': 'Tema eliminado correctamente.'
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se pudo eliminar la metodología DUA.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # TODO: Investigate how form url path with django-filters
    #   and form the path but with the id of the topic
    #       and by the way investigate about the search options on DRF

    # PROVISIONAL
    @action(detail=False, methods=['POST'], url_path='type')
    def get_topics_by_type(self, request):
        if request.data:
            if 1 <= int(request.data['type']) <= 3:
                topics = self.get_serializer().Meta.model.objects.get_topics_by_type(
                    type=request.data['type']
                )

                if topics is not None:
                    topic_serializer = self.get_serializer(topics, many=True)

                    return Response(
                        {
                            'ok': True,
                            'conon_data': topic_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:

                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se pudo encontrar los Temas correspondientes.'
                        },
                        status=status.HTTP_200_OK
                    )
            else:

                return Response(
                    {
                        'ok': False,
                        'detail': 'El tipo de tema no ha sido enviado.'
                    },
                    status=status.HTTP_200_OK
                )

    @action(detail=True, methods=['PUT'], url_path='block-topic')
    def block_topic(self, request, pk=None):
        topic = self.get_queryset(pk=pk)
        if topic is not None:
            topic.active = False
            topic.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Tema de Estudio bloqueado correctamente.'
                }
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró el Tema de Estudio'
            }
        )

    @action(detail=False, methods=['DELETE'], url_path='destroy-topics')
    def destroy_many_topics(self, request):

        if request.data:
            if request.data['topics']:
                topics = self.get_serializer().Meta.model.objects.get_many_topics(
                    request.data['topics']
                )
                if topics is not None:
                    for topic in topics:
                        topic.active = False
                        topic.auth_state = 'I'

                    self.get_serializer().Meta.model.objects.bulk_update(topics, ['active', 'auth_state'])

                    return Response(
                        {
                            'ok': True,
                            'message': 'Temas de Estudio eliminados correctamente.'
                        },
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo eliminar a los respectivos de Temas de Estudio.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontraron las llaves de los Temas a eliminar.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío la correspondiente información.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # TODO: Encontrar la manera de crear el siguiente enlace vía GET

    @action(detail=True, methods=['POST'], url_path='new-students')
    def get_new_teachers_for_area(self, request, pk=None):
        students = self.get_serializer().Meta.model.objects.get_students_by_topic_id(pk=pk, active=True)

        if students is not None:
            if request.data:
                student_serializer = StudentShortListSerializer(
                    Student.objects.get_student_short_data(age=request.data['age']), many=True
                )
            else:
                student_serializer = StudentShortListSerializer(
                    Student.objects.get_student_short_data(), many=True
                )
            topic_student_serializer = StudentsForManyChoicesSerializer(students, many=True)
            valid_students = [
                student for student in student_serializer.data
                if student not in topic_student_serializer.data
            ]
            return Response(
                {
                    'ok': True,
                    'conon_data': valid_students
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se pudo cargar los Estudiantes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['POST'], url_path='assign-students')
    def save_students_to_topic(self, request, pk=None):
        topic = self.get_queryset(pk)

        if topic is not None:
            if request.data['students']:
                for student in request.data['students']:
                    topic.students.add(student)
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar a los Estudiante/s.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    'ok': True,
                    'message': 'Estudiante/s agregados correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # TODO: Encontrar la manera crear rutas con argumentos que no son campos de una modelos

    @action(detail=True, methods=['GET'], url_path='by-teacher')
    def get_topics_by_teacher_id(self, request, pk=None):
        user = Teacher.objects.get_user_id_by_teacher(pk=pk)
        if user is not None:
            if user['person__user']:
                user_id = user['person__user']
                topics = self.get_serializer().Meta.model.objects.get_topics_by_owner(user=user_id)

                if topics is not None:
                    topic_serializer = self.get_serializer(topics, many=True)

                    return Response(
                        {
                            'ok': True,
                            'conon_data': topic_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontraron Temas de Estudio.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encuentra el Usuario.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se encontró el Docente.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['GET'], url_path='students')
    def get_students_list_by_topic(self, request, pk=None):
        students = self.get_serializer().Meta.model.objects.get_students_by_topic_id(pk=pk)

        if students is not None:
            topic_student_serializer = StudentsForManyChoicesSerializer(students, many=True)

            return Response(
                {
                    'ok': True,
                    'conon_data': topic_student_serializer.data
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se pudo cargar los Estudiantes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
