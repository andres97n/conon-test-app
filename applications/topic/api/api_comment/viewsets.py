from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import CommentSerializer
from applications.base.permissions import IsOwner
from applications.base.paginations import CononShortPagination

# TODO: Pendiente en poner los permisos para los diferentes métodos y
#   que información retorna.


class CommentViewSet(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]
    pagination_class = CononShortPagination

    # Return Comment Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_comment_list()
        return self.get_serializer().Meta.model.objects.get_comment_by_id(pk)

    # Get Comment List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        comment_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': comment_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create a Comment
    def create(self, request, *args, **kwargs):
        comment_serializer = self.get_serializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Comentario creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': comment_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update a Comment
    def update(self, request, pk=None, *args, **kwargs):
        comment = self.get_queryset(pk)
        if comment:
            # Send information to serializer referencing the instance
            comment_serializer = self.get_serializer(comment, data=request.data)
            if comment_serializer.is_valid():
                comment_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': comment_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': comment_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Comentario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Comment
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            comment_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': comment_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Comentario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Comment
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        comment = self.get_queryset(pk)
        if comment:
            comment.active = False
            comment.auth_state = 'I'
            comment.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Comentario eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Comentario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
