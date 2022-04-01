
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.users.models import Conversation, Conversation_Detail
from .serializers import ConversationListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_messages_count(request, user):
    if request.method == 'GET':
        if user:
            user_count = Conversation_Detail.objects.not_view_messages_owner(user=user)
            print(user_count)
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
            if search:
                if search == 'all':
                    user_first = Conversation.objects.user_exists_like_first_in_conversation(user=user)
                    user_second = Conversation.objects.user_exists_like_second_in_conversation(user=user)
                elif search == 'unanswered':
                    user_first = Conversation.objects.user_exists_like_first_in_conversation(user=user).\
                        filter(state=0)
                    user_second = Conversation.objects.user_exists_like_second_in_conversation(user=user).\
                        filter(state=0)
            else:
                user_first = Conversation.objects.user_exists_like_first_in_conversation(user=user).\
                    filter(conversation_detail__state=0)
                user_second = Conversation.objects.user_exists_like_second_in_conversation(user=user).\
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
