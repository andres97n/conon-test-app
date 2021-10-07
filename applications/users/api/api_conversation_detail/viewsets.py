from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from applications.base.permissions import IsOwner
from .serializers import ConversationDetailSerializer


class ConversationDetailViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsOwner])
    serializer_class = ConversationDetailSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_conversation_detail_list()
        return self.get_serializer().Meta.model.objects.get_conversation_detail_by_pk(pk)

    # Get Conversation Detail List
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

    # Create Message
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        conversation_detail_serializer = self.get_serializer(data=request.data)
        if conversation_detail_serializer.is_valid():
            conversation_detail_serializer.save()

            return Response(
                {
                    'ok': True,
                    'detail': 'Mensaje enviado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': conversation_detail_serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Message
    def update(self, request, pk=None, *args, **kwargs):
        message = self.get_queryset(pk)
        if message:
            # Send information to serializer referencing the instance
            conversation_detail_serializer = self.get_serializer(message, data=request.data)
            if conversation_detail_serializer.is_valid():
                conversation_detail_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': conversation_detail_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': conversation_detail_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Mensaje.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Message Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            conversation_detail_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': conversation_detail_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Mensaje.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Message
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        conversation_detail = self.get_queryset(pk)
        if conversation_detail:
            conversation_detail.blocked = True
            conversation_detail.auth_state = 'I'
            conversation_detail.save()

            return Response(
                {
                    'ok': True,
                    'detail': 'Mensaje eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Mensaje.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

