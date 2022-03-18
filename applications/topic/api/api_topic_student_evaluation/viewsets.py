from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsTeacherOrIsStudent
from applications.base.paginations import CononPagination
from .serializers import TopicStudentEvaluationSerializer, TopicStudentEvaluationListSerializer


class TopicStudentEvaluationViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsTeacherOrIsStudent])
    serializer_class = TopicStudentEvaluationSerializer
    list_serializer_class = TopicStudentEvaluationListSerializer
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic', 'user', 'active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects. \
            get_topic_student_evaluation_list()

    # Get Problem Resolution List
    def list(self, request):
        topic_student_evaluation_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(topic_student_evaluation_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        topic_student_evaluation_serializer = self.list_serializer_class(
            topic_student_evaluation_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': topic_student_evaluation_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Topic Student Evaluation
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        topic_student_evaluation_serializer = self.get_serializer(data=request.data)
        if topic_student_evaluation_serializer.is_valid():
            topic_student_evaluation_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': topic_student_evaluation_serializer.data['id'],
                    'message': 'Autoevaluación creada correctamente.'
                    if topic_student_evaluation_serializer.data['type'] == 1
                    else 'Coevaluación creada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': topic_student_evaluation_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Topic Student Evaluation
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_topic_student_evaluation(self, request, pk=None):
        topic_student_evaluation = self.get_object(pk)
        topic_student_evaluation.active = False
        topic_student_evaluation.save()

        return Response(
            {
                'ok': True,
                'message': 'Autoevaluación bloqueada correctamente.'
                if topic_student_evaluation.type == 1
                else 'Coevaluación bloqueada correctamente'
            },
            status=status.HTTP_200_OK
        )
