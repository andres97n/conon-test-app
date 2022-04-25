
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.users.models import Teacher, Conversation
from applications.school.models import Classroom, AsignatureClassroom
from applications.users.api.api_student.serializers import StudentShorListByConversationSerializer
from .serializers import TeacherShorListByConversation
from applications.users.api.api_conversation.serializers import (
    ConversationFirstUserShortListSerializer, ConversationSecondUserShortListSerializer)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_conversation_for_teacher(request, user, school_period):
    if request.method == 'GET':
        if user and school_period:
            teacher = Teacher.objects.get_teacher_object_by_user(user=user)
            if teacher is not None:
                asignature_classroom = AsignatureClassroom.objects.get_classrooms_by_teacher(
                    teacher=teacher.id, period=school_period
                )
                if asignature_classroom is not None:
                    available_users = []
                    for data in asignature_classroom:
                        students = Classroom.objects.get_students_by_classroom_id(pk=data.classroom.id)
                        if students is not None:
                            student_serializer = StudentShorListByConversationSerializer(
                                students, many=True
                            )
                            for student in student_serializer.data:
                                available_users.append(student)
                    search_users = []
                    [search_users.append(x) for x in available_users if x not in search_users]
                    teachers = Teacher.objects.get_teacher_list_exclude_owner(
                        owner=teacher.id
                    )
                    if teachers is not None:
                        teacher_serializer = TeacherShorListByConversation(
                            teachers, many=True
                        )
                        for item in teacher_serializer.data:
                            search_users.append(item)
                    conversation = Conversation.objects.get_conversations_by_user_id(user=user)
                    if conversation is not None:
                        conversation_first_user_serializer = ConversationFirstUserShortListSerializer(
                            conversation['first_user'], many=True
                        )
                        conversation_second_user_serializer = ConversationFirstUserShortListSerializer(
                            conversation['second_user'], many=True
                        )
                        search_users = [
                            user for user in search_users
                            if user['id'] not in conversation_first_user_serializer.data
                        ]
                        search_users = [
                            user for user in search_users
                            if user['id'] not in conversation_second_user_serializer.data
                        ]
                    return Response(
                        {
                            'ok': True,
                            'conon_data': search_users
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se encontró las Aulas asignadas al Docente.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el Docente correspondiente.'
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
