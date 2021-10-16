from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import ReplySerializer
from applications.base.permissions import IsOwner
from applications.base.paginations import CononShortPagination


class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    pagination_class = CononShortPagination
    permission_classes = ([IsOwner])

    # Return Comment Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_reply_list()
        return self.get_serializer().Meta.model.objects.get_reply_by_id(pk)

    # Get Reply List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        reply_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': reply_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create a Reply
    def create(self, request, *args, **kwargs):
        reply_serializer = self.get_serializer(data=request.data)
        if reply_serializer.is_valid():
            reply_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Respuesta creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': reply_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update a Reply
    def update(self, request, pk=None, *args, **kwargs):
        reply = self.get_queryset(pk)
        if reply:
            # Send information to serializer referencing the instance
            reply_serializer = self.get_serializer(reply, data=request.data)
            if reply_serializer.is_valid():
                reply_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': reply_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': reply_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Respuesta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Reply
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            reply_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': reply_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Respuesta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Reply
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        reply = self.get_queryset(pk)
        if reply:
            reply.state = False
            reply.auth_state = 'I'
            reply.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Respuesta eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Respuesta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
