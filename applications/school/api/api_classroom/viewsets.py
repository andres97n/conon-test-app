from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from applications.base.paginations import CononPagination
from applications.users.models import Student
from applications.school.api.api_classroom.serializers import ClassroomSerializer, \
    StudentsForManyChoicesSerializer, ClassroomShortSerializer
from applications.users.api.api_student.serializers import StudentShortListSerializer


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
