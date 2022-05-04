
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import SpokesmanQuestionAcSerializer, SpokesmanQuestionAcListSerializer


class SpokesmanQuestionAcViewSet(viewsets.GenericViewSet):
    serializer_class = SpokesmanQuestionAcSerializer
    list_serializer_class = SpokesmanQuestionAcListSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_spokesman_question_ac_active_queryset(),
            id=pk
        )

    # Return Spokesman Question Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_spokesman_question_ac_list()

    # Get Spokesman Question Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        spokesman_question_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': spokesman_question_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Spokesman Question Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        spokesman_question_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if spokesman_question_ac_serializer.is_valid():
            spokesman_question_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'spokesman_question_ac':
                        spokesman_question_ac_serializer.data
                        if isinstance(spokesman_question_ac_serializer.data, list)
                        else spokesman_question_ac_serializer.data['id'],
                    'message':
                        'Preguntas agregadas correctamente'
                        if isinstance(spokesman_question_ac_serializer.data, list)
                        else 'Pregunta agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': spokesman_question_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Spokesman Question Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_spokesman_question_ac(self, request, pk=None):
        spokesman_question_ac = self.get_object(pk)
        spokesman_question_ac.active = False
        spokesman_question_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Pregunta bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )
