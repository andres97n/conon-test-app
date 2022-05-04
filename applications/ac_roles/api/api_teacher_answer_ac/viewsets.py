

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import TeacherAnswerAcSerializer, TeacherAnswerAcListSerializer


class TeacherAnswerAcViewSet(viewsets.GenericViewSet):
    serializer_class = TeacherAnswerAcSerializer
    list_serializer_class = TeacherAnswerAcListSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher', 'spokesman_question_ac', 'active']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.get_teacher_answer_ac_active_queryset(),
            id=pk
        )

    # Return Teacher Answer Ac
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_teacher_answer_ac_list()

    # Get Teacher Answer Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        teacher_answer_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': teacher_answer_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Teacher Answer Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        teacher_answer_ac_serializer = self.get_serializer(
            data=request.data, many=is_many
        )
        if teacher_answer_ac_serializer.is_valid():
            teacher_answer_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'teacher_answer_ac':
                        teacher_answer_ac_serializer.data
                        if isinstance(teacher_answer_ac_serializer.data, list)
                        else teacher_answer_ac_serializer.data['id'],
                    'message':
                        'Respuestas agregadas correctamente'
                        if isinstance(teacher_answer_ac_serializer.data, list)
                        else 'Respuesta agregada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': teacher_answer_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Teacher Answer Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_teacher_answer_ac(self, request, pk=None):
        teacher_answer_ac = self.get_object(pk)
        teacher_answer_ac.active = False
        teacher_answer_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Respuesta bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )

