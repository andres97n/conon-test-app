from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsTeacher
from applications.base.paginations import CononPagination
from applications.users.models import Student, Teacher
from applications.school.api.api_classroom.serializers import ClassroomSerializer, \
    StudentsForManyChoicesSerializer, ClassroomShortSerializer
from applications.users.api.api_student.serializers import StudentShortListSerializer


class ClassroomViewSet(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = ClassroomSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state']

    # Get Classroom Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_classroom_list()
        return self.get_serializer().Meta.model.objects.get_classroom_by_id(pk)

# TODO: Mejorar el siguiente código

    def get_permissions(self):
        if self.action == 'get_classrooms_list_by_teacher' or self.action == 'get_new_students_for_classrooms':
            self.permission_classes = [IsTeacher]
        elif self.action == 'save_students_for_classroom' or self.action == 'get_students_list_by_classroom':
            self.permission_classes = [IsTeacher]
        elif self.action == 'block_students_by_classroom' or 'get_classrooms_list_by_teacher':
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAdminUser]

        return [permission() for permission in self.permission_classes]

    # Get Classroom List
    def list(self, request, *args, **kwargs):
        classroom_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(classroom_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        classroom_serializer = self.get_serializer(classroom_queryset, many=True)

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
                    'id': classroom_serializer.data['id'],
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
            classroom.state = 0
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

    @action(detail=True, methods=['POST'], url_path='assign-students')
    def save_students_for_classroom(self, request, pk=None):
        classroom = self.get_queryset(pk)

        if classroom is not None:
            if request.data['students']:
                for student in request.data['students']:
                    classroom.students.add(student)
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
                'detail': 'No existe esta Área de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['DELETE'], url_path='destroy-classrooms')
    def destroy_many_classrooms(self, request):
        classrooms = self.get_serializer().Meta.model.objects.get_many_classrooms(
            classrooms=request.data['classrooms']
        )
        if classrooms:
            for classroom in classrooms:
                classroom.state = 0
                classroom.auth_state = 'I'

            self.get_serializer().Meta.model.objects.bulk_update(
                classrooms, ['state', 'auth_state']
            )

            return Response(
                {
                    'ok': True,
                    'message': 'Aulas eliminadas correctamente.'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se puede eliminar las siguientes Aulas.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['GET'], url_path='active')
    def get_classrooms_active(self, request):
        classrooms = self.get_serializer().Meta.model.objects.get_classroom_active_list()
        if classrooms:
            classroom_serializer = self.get_serializer(classrooms, many=True)
            return Response(
                {
                    'ok': True,
                    'conon_data': classroom_serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se puedo retornar las siguientes Aulas.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # TODO: Cambiar el método de lista por uno correcto
    @action(detail=True, methods=['POST'], url_path='new-students')
    def get_new_students_for_classrooms(self, request, pk=None):
        students = self.get_serializer().Meta.model.objects.get_students_by_classroom_id(pk=pk)
        if students is not None:
            if request.data:
                student_serializer = StudentShortListSerializer(
                    Student.objects.get_student_short_data(age=request.data['age']), many=True
                )
            else:
                student_serializer = StudentShortListSerializer(
                    Student.objects.get_student_short_data(), many=True
                )
            classroom_student_serializer = StudentsForManyChoicesSerializer(students, many=True)
            valid_students = [
                student for student in student_serializer.data
                if student not in classroom_student_serializer.data
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

    @action(detail=False, methods=['GET'], url_path='short')
    def get_classrooms_short_data(self, request):
        classrooms = self.get_serializer().Meta.model.objects.get_short_classroom()
        if classrooms is not None:
            classroom_serializer = ClassroomShortSerializer(classrooms, many=True)

            return Response(
                {
                    'ok': True,
                    'conon_data': classroom_serializer.data
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

    @action(detail=False, methods=['POST'], url_path='by-teacher')
    def get_classrooms_list_by_teacher(self, request):

        if request.data:
            teacher = Teacher.objects.get_teacher_by_user(pk=request.data['user'])

            if teacher is not None:
                classrooms = self.get_serializer().Meta.model.objects. \
                    get_classrooms_by_teacher(pk=teacher['id'])

                if classrooms is not None:
                    classroom_serializer = self.get_serializer(classrooms, many=True)

                    return Response(
                        {
                            'ok': True,
                            'conon_data': classroom_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontró el Docente en presentes Aulas.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró al usuario enviado dentro de los Docentes.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Docente en la petición.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['GET'], url_path='students')
    def get_students_list_by_classroom(self, request, pk=None):
        students = self.get_serializer().Meta.model.objects.get_students_by_classroom_id(pk=pk)

        if students is not None:
            classroom_serializer = StudentsForManyChoicesSerializer(students, many=True)

            return Response(
                {
                    'ok': True,
                    'conon_data': classroom_serializer.data
                }
            )
        else:

            return Response(
                {
                    'ok': False,
                    'detail': 'No se encontró la correspondiente Aula.'
                }
            )

    @action(detail=True, methods=['DELETE'], url_path='block-students')
    def block_students_by_classroom(self, request, pk=None):

        if request.data:
            students = self.get_serializer().Meta.model.objects.get_students_by_classroom_id(pk=pk)
            classroom = self.get_queryset(pk=pk)
            validate_students = True
            print(students)
            print(request.data['students'])
            for student in students:
                if student['students'] not in request.data['students']:
                    validate_students = False

            if validate_students:
                for student in request.data['students']:
                    student_query = Student.objects.get_student_detail_data(pk=student)
                    classroom.students.remove(student_query)

                return Response(
                    {
                        'ok': True,
                        'message': 'Estudiantes eliminados correctamente.'
                    },
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encuentran estudiantes enviados dentro del Aula.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío las referencias de los Estudiantes a bloquear.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

