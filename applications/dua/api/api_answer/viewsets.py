from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import AnswerSerializer
from applications.base.permissions import IsOwnerAndStudent
from applications.base.paginations import CononPagination


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = ([IsOwnerAndStudent])
    pagination_class = CononPagination

    # Return Answer
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_answer_list()
        return self.get_serializer().Meta.model.objects.get_answer_by_id(pk)

    # Get Answer List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        answer_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': answer_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Answer
    def create(self, request, *args, **kwargs):
        is_many = True if isinstance(request.data, list) else False
        answer_serializer = self.get_serializer(data=request.data, many=is_many)
        if answer_serializer.is_valid():
            answer_serializer.save()

            return Response(
                {
                    'ok': True,
                    'answer':
                        answer_serializer.data
                        if isinstance(answer_serializer.data, list)
                        else answer_serializer.data['id'],
                    'message':
                        'Respuestas agregadas correctamente'
                        if isinstance(answer_serializer.data, list)
                        else 'Respuesta agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': answer_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Answer
    def update(self, request, pk=None, *args, **kwargs):
        answer = self.get_queryset(pk)
        if answer:
            # Send information to serializer referencing the instance
            answer_serializer = self.get_serializer(answer, data=request.data)
            if answer_serializer.is_valid():
                answer_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': answer_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': answer_serializer.errors,
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

    # Detail Answer
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            answer_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': answer_serializer.data,
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

    # Delete Answer
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        answer = self.get_queryset(pk)
        if answer:
            answer.auth_state = 'I'
            answer.save()

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

    # Block Answer
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_answer(self, request, pk=None):
        answer = get_object_or_404(self.serializer_class.Meta.model, id=pk)
        answer.active = False
        answer.save()
        return Response(
            {
                'ok': True,
                'message': 'Respuesta bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
