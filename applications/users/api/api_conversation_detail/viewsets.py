from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsOwner
from applications.base.paginations import CononPagination
from .serializers import ConversationDetailSerializer, ConversationDetailListSerializer


class ConversationDetailViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsOwner])
    serializer_class = ConversationDetailSerializer
    list_serializer_class = ConversationDetailListSerializer
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation', 'block']

    # Get Conversation Data
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_active_conversation_detail(), id=pk
        )

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.get_conversation_detail_list()

    # Get Conversation Detail List
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

    # Create Message
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        conversation_detail_serializer = self.get_serializer(data=request.data)
        if conversation_detail_serializer.is_valid():
            conversation_detail_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': conversation_detail_serializer.data['id'],
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

    # Delete Message
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        conversation_detail = self.get_object(pk)
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

    # Block Conversation Detail
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_conversation_detail(self, request, pk=None):
        conversation_detail = self.get_object(pk)
        conversation_detail.active = False
        conversation_detail.save()

        return Response(
            {
                'ok': True,
                'message': 'Mensaje bloqueado correctamente.'
            },
            status=status.HTTP_200_OK
        )
