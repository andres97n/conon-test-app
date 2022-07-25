
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.users.models import Student, Conversation
from applications.school.models import Classroom, AsignatureClassroom
from applications.users.api.api_teacher.serializers import TeacherForConversationSerializer
from .serializers import (StudentSerializer, StudentsByNewConversationSerializer)
from applications.users.api.api_conversation.serializers import ConversationListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_by_user(request, user):
    if request.method == 'GET':
        if user:
            student = Student.objects.get_student_by_user_object(user)
            if student:
                student_serializer = StudentSerializer(student)
                return Response(
                    {
                        'ok': True,
                        'detail': student_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontro el Estudiante.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Usuario.'
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


"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_conversation_for_student(request, user, school_period):
    if request.method == 'GET':
        if user and school_period:
            student = Student.objects.get_student_object_by_user(user=user)
            if student is not None:
                classroom = Classroom.objects.get_classroom_by_student_and_period(
                    period=school_period, student=student.id
                )
                if classroom is not None:
                    students = Classroom.objects.get_students_by_classroom_id(pk=classroom.id)
                    if students is not None:
                        student_serializer = StudentObjectShotListSerializer(students, many=True)
                        asignature_classroom = AsignatureClassroom.objects.\
                            get_asignature_classroom_by_classroom(classroom=classroom.id)
                        if asignature_classroom is not None:
                            available_users = []
                            teacher_serializer = TeacherObjectShortSerializer(
                                asignature_classroom, many=True
                            )
                            for student in student_serializer.data:
                                available_users.append(student)
                            for teacher in teacher_serializer.data:
                                available_users.append(teacher)
                            return Response(
                                {
                                    'ok': True,
                                    'conon_data': available_users
                                },
                                status=status.HTTP_200_OK
                            )
                        else:
                            return Response(
                                {
                                    'ok': False,
                                    'detail': 'No se encontró los docentes.'
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontró los estudiantes.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontró el Aula correspondiente, revise la referencia.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el Estudiante, revise la referencia enviada.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron las referencias requeridas para la consulta.'
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
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_conversation_for_student(request, user, school_period):
    if request.method == 'GET':
        if user and school_period:
            user_first = Conversation.objects.user_exists_like_first_in_conversation(user=user)
            user_second = Conversation.objects.user_exists_like_second_in_conversation(user=user)
            if user_first is not None and user_second is not None:
                users_listed = []
                available_users = []
                user_first_serializer = ConversationListSerializer(user_first, many=True)
                user_second_serializer = ConversationListSerializer(user_second, many=True)
                for conversation in user_first_serializer.data:
                    if conversation['first_user']['id'] != user:
                        first_user = conversation['first_user']
                        users_listed.append(first_user)
                    else:
                        second_user = conversation['second_user']
                        users_listed.append(second_user)
                for conversation in user_second_serializer.data:
                    if conversation['first_user']['id'] != user:
                        first_user = conversation['first_user']
                        users_listed.append(first_user)
                    else:
                        second_user = conversation['second_user']
                        users_listed.append(second_user)
                student = Student.objects.get_student_object_by_user(user=user)
                if student is not None:
                    classroom = Classroom.objects.get_classroom_by_student_and_period(
                        period=school_period, student=student.id
                    )
                    if classroom is not None:
                        users_list = []
                        available_users = []
                        students = Classroom.objects.get_students_by_classroom_id(pk=classroom.id)
                        if students is not None:
                            student_serializer = StudentsByNewConversationSerializer(
                                students, many=True
                            )
                            asignature_classroom = AsignatureClassroom.objects. \
                                get_asignature_classroom_by_classroom(classroom=classroom.id)
                            if asignature_classroom is not None:
                                teacher_serializer = TeacherForConversationSerializer(
                                    asignature_classroom, many=True
                                )
                                [users_list.append(student) for student in student_serializer.data
                                 if student not in users_listed]
                                [users_list.append(teacher) for teacher in teacher_serializer.data
                                 if teacher not in users_listed]
                                for user in users_list:
                                    if user['id'] not in users_list:
                                        available_users.append(user)

                                return Response(
                                    {
                                        'ok': True,
                                        'conon_data': available_users
                                    },
                                    status=status.HTTP_200_OK
                                )
                            else:
                                return Response(
                                    {
                                        'ok': False,
                                        'detail': 'No se encontró los respectivos docentes.'
                                    },
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                        else:
                            return Response(
                                {
                                    'ok': False,
                                    'detail': 'No se encontró la respectiva aula.'
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        return Response(
                            {
                                'ok': False,
                                'detail': 'No se encontró el Aula correspondiente, revise la referencia.'
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se pudo encontrar el estudiante enviado.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar las conversaciones del usuario.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron las referencias requeridas para la consulta.'
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
