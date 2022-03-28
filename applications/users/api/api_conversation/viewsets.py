from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import ConversationSerializer, ConversationListSerializer
from applications.base.permissions import IsTeacherOrIsStudent
from applications.base.paginations import CononPagination


class ConversationViewSet(LoggingMixin, viewsets.GenericViewSet):
    permission_classes = ([IsTeacherOrIsStudent])
    serializer_class = ConversationSerializer
    list_serializer_class = ConversationListSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'block']

    # Get Conversation Data
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_active_conversation(), id=pk
        )

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.get_conversation_list()

    # Get Conversation List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        conversation_detail_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': conversation_detail_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Conversation
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        conversation_serializer = self.get_serializer(data=request.data)
        if conversation_serializer.is_valid():
            conversation_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': conversation_serializer.data['id'],
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

    # Delete Conversation
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        conversation = self.get_object(pk)
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

    # Block Conversation
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_conversation(self, request, pk=None):
        conversation = self.get_object(pk)
        conversation.active = False
        conversation.save()

        return Response(
            {
                'ok': True,
                'message': 'Conversación bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
