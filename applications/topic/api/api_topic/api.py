
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.users.models import Person, Student
from applications.topic.models import Topic
from applications.school.models import SchoolPeriod, Classroom
from applications.base.permissions import IsTeacher
from .serializers import TopicSerializer, TopicStudentsListSerializer, TopicShortListSerializer
from applications.school.api.api_classroom.serializers import StudentsByClassroomForGroupsSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_topics_list_by_student(request, user):
    if request.method == 'GET':
        if user:
            person = Person.objects.get_person_by_user(user)
            if person and person.student:
                school_period = SchoolPeriod.objects.get_period_active()
                if school_period is not None:
                    topics = Topic.objects.get_topics_by_students(
                        person.student.id, school_period.id
                    )
                    topic_serializer = TopicSerializer(topics, many=True)

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
                            'detail': 'No se encontró el Período Lectivo.'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el Usuario.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envio la información necesaria.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_topics_list_by_student(request, user):
    if request.method == 'GET':
        if user:
            person = Person.objects.get_person_by_user(user)
            if person and person.student:
                school_period = SchoolPeriod.objects.get_period_active()
                if school_period is not None:
                    topics = Topic.objects.get_current_topics_by_students(
                        person.student.id, school_period
                    )
                    topic_serializer = TopicSerializer(topics, many=True)

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
                            'detail': 'No se encontró un Período Lectivo activo.'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró la información del Usuario.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envio la información necesaria.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_new_students_for_topic(request, topic, classroom):
    if request.method == 'GET':
        if topic and classroom:
            students = Topic.objects.get_students_by_topic_id(pk=topic, active=True)
            if students is not None:
                classroom_students = Classroom.objects.get_students_by_classroom_id(pk=classroom)
                if classroom_students is not None:
                    students_serializer = StudentsByClassroomForGroupsSerializer(
                        students, many=True
                    )
                    classroom_students_serializer = StudentsByClassroomForGroupsSerializer(
                        classroom_students, many=True
                    )
                    valid_students = [
                        student for student in classroom_students_serializer.data
                        if student not in students_serializer.data
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
                            'detail': 'No se encontró el Aula.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo cargar los Estudiantes.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron las referencias necesarias para la consulta.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])
@permission_classes([IsTeacher])
def get_students_by_topic(request, topic):
    if request.method == 'GET':
        if topic:
            students = Topic.objects.get_students_by_topic_id(pk=topic, active=False)
            if students is not None:
                if len(students) == 0:
                    return Response(
                        {
                            'ok': True,
                            'conon_data': []
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    students_serializer = TopicStudentsListSerializer(students, many=True)
                    return Response(
                        {
                            'ok': True,
                            'conon_data': students_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar los estudiantes, por favor '
                                  'revise el tópico enviado.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envió el Tópico.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_inactive_topics_list_by_student(request, user, school_period):
    if request.method == 'GET':
        if user and school_period:
            student = Student.objects.get_student_by_user_object(user=user)
            if student is not None:
                topic = Topic.objects.get_inactive_topics_by_student(
                    student_id=student.id, period_id=school_period
                )
                if topic is not None:
                    topic_serializer = TopicShortListSerializer(topic, many=True)

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
                            'detail': 'No se encontró el tópico.'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el estudiante.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los valores necesarios.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
