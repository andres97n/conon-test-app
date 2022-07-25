
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.users.models import Conversation, Conversation_Detail, Teacher
from applications.school.models import AsignatureClassroom, Classroom
from .serializers import ConversationListSerializer
from applications.users.api.api_student.serializers import StudentsByNewConversationSerializer
from applications.users.api.api_teacher.serializers import TeacherForNewConversation


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_messages_count(request, user):
    if request.method == 'GET':
        if user:
            user_count = Conversation_Detail.objects.not_view_messages_owner(user=user)
            if user_count is not None:
                return Response(
                    {
                        'ok': True,
                        'conon_data': user_count
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encuentran conversaciones de este Usuario, revise la '
                                  'referencia enviada.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_conversations_list(request, user, search):
    if request.method == 'GET':
        if user:
            user_first = []
            user_second = []
            if search == 'all':
                user_first = Conversation.objects.user_exists_like_first_in_conversation(user=user)
                user_second = Conversation.objects.user_exists_like_second_in_conversation(user=user)
            elif search == 'unanswered':
                user_first = Conversation.objects.user_exists_like_first_in_conversation(user=user). \
                    filter(state=0)
                user_second = Conversation.objects.user_exists_like_second_in_conversation(user=user). \
                    filter(state=0)
            else:
                user_first = Conversation.objects.user_exists_like_first_in_conversation(user=user). \
                    filter(conversation_detail__state=0)
                user_second = Conversation.objects.user_exists_like_second_in_conversation(user=user). \
                    filter(conversation_detail__state=0)
            if user_first is not None and user_second is not None:
                user_first_serializer = ConversationListSerializer(user_first, many=True)
                user_second_serializer = ConversationListSerializer(user_second, many=True)
                user_conversations = []
                if len(user_second_serializer.data) > 0 or len(user_first_serializer.data) > 0:
                    for student in user_first_serializer.data:
                        user_conversations.append(student)
                    for student in user_second_serializer.data:
                        user_conversations.append(student)
                    return Response(
                        {
                            'ok': True,
                            'conon_data': user_conversations
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': True,
                            'conon_data': user_conversations
                        },
                        status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'Por favor revise la referencia del Usuario enviada, '
                                  'ocurrió un error.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_current_conversations_list(request, user):
    if request.method == 'GET':
        if user:
            user_first = Conversation.objects.user_exists_like_first_in_conversation(user=user)
            user_second = Conversation.objects.user_exists_like_second_in_conversation(user=user)
            if user_first is not None and user_second is not None:
                user_conversations = []
                user_first_serializer = ConversationListSerializer(user_first, many=True)
                user_second_serializer = ConversationListSerializer(user_second, many=True)
                for student in user_first_serializer.data:
                    user_conversations.append(student)
                for student in user_second_serializer.data:
                    user_conversations.append(student)
                return Response(
                    {
                        'ok': True,
                        'conon_data': user_conversations
                    },
                    status=status.HTTP_200_OK
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_user_conversations_list(request, user, school_period):
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
                teacher = Teacher.objects.get_teacher_object_by_user(user=user)
                if teacher is not None:
                    asignature_classroom = AsignatureClassroom.objects.get_classrooms_by_teacher(
                        teacher=teacher.id, period=school_period
                    )
                    if asignature_classroom is not None:
                        users_list = []
                        for data in asignature_classroom:
                            students = Classroom.objects.get_students_by_classroom_id(
                                pk=data.classroom.id
                            )
                            if students is not None:
                                student_serializer = StudentsByNewConversationSerializer(
                                    students, many=True
                                )
                                [users_list.append(student) for student in student_serializer.data
                                 if student not in users_listed]
                        teachers = Teacher.objects.get_teacher_list_exclude_owner(
                            owner=teacher.id
                        )
                        if teachers is not None:
                            teacher_serializer = TeacherForNewConversation(
                                teachers, many=True
                            )
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
                                'detail': 'No se encontró las Aulas asignadas al Docente.'
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se enconctró el docente.'
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
