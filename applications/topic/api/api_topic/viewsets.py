from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import TopicSerializer
from applications.base.permissions import IsOwnerAndTeacher
from applications.base.paginations import CononShortPagination


class TopicViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsOwnerAndTeacher])
    serializer_class = TopicSerializer
    pagination_class = CononShortPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Return Topic Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_topic_list()
        return self.get_serializer().Meta.model.objects.get_topic_by_id(pk)

    # Get Topic List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        topic_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': topic_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create a Topic
    def create(self, request, *args, **kwargs):
        topic_serializer = self.get_serializer(data=request.data)
        if topic_serializer.is_valid():
            topic_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Tema creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': topic_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update a Topic
    def update(self, request, pk=None, *args, **kwargs):
        topic = self.get_queryset(pk)
        if topic:
            # Send information to serializer referencing the instance
            topic_serializer = self.get_serializer(topic, data=request.data)
            if topic_serializer.is_valid():
                topic_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': topic_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': topic_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Topic
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            topic_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': topic_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Topic
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        topic = self.get_queryset(pk)
        if topic:
            topic.active = False
            topic.auth_state = 'I'
            topic.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Tema eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
