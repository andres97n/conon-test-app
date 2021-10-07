from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from applications.base.permissions import IsTeacherOrIsStudent
from .serializers import ConversationSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsTeacherOrIsStudent])
    serializer_class = ConversationSerializer

    # Get Conversation Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_conversation_list()
        return self.get_serializer().Meta.model.objects.get_conversation_by_pk(pk)

    # Get Conversation List
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

    def create(self, request, *args, **kwargs):
        # Send information to serializer
        conversation_serializer = self.get_serializer(data=request.data)
        if conversation_serializer.is_valid():
            conversation_serializer.save()

            return Response(
                {
                    'ok': True,
                    'detail': 'Conversación creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': conversation_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Conversation
    def update(self, request, pk=None, *args, **kwargs):
        conversation = self.get_queryset(pk)
        if conversation:
            # Send information to serializer referencing the instance
            conversation_serializer = self.get_serializer(conversation, data=request.data)
            if conversation_serializer.is_valid():
                conversation_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': conversation_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': conversation_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Conversación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Conversation Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            conversation_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': conversation_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Conversación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Conversation
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        conversation = self.get_queryset(pk)
        if conversation:
            conversation.blocked = True
            conversation.auth_state = 'I'
            conversation.save()

            return Response(
                {
                    'ok': True,
                    'detail': 'Conversación eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Conversación.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

